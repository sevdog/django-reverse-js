import json
from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str
from django.urls import get_script_prefix, get_ns_resolver
from .conf import settings


def prepare_url_list(urlresolver, namespace_path='', namespace=''):
    """
    Builds namespace urls and patterns recurively in the following form::
       [(<url_name>, <url_patern_tuple> ), ...]
    """
    exclude_ns = settings.JS_EXCLUDE_NAMESPACES
    include_only_ns = settings.JS_INCLUDE_ONLY_NAMESPACES

    if exclude_ns and include_only_ns:
        raise ImproperlyConfigured(
            'Usage of both REVERSEJS_EXCLUDE_NAMESPACES '
            'and REVERSEJS_INCLUDE_ONLY_NAMESPACES '
            'is not allowed, please use just one of these settings.'
        )

    # expect namespace in the form of "namespace:"
    simple_namespace = namespace[:-1] if namespace.endswith(':') else namespace
    if simple_namespace in exclude_ns:
        return

    if include_only_ns:
        # Test urls without namespace
        in_on_empty_ns = namespace == '' and '' in include_only_ns

        # check if nestead ns isn't subns of include_only ns
        # e.g. ns = "foo:bar" include_only = ["foo"] -> this ns will be used
        # works for ns = "lorem:ipsum:dolor" include_only = ["lorem:ipsum"]
        # ns "lorem" will be ignored but "lorem:ipsum" & "lorem:ipsum:.." won't
        in_on_is_in_list = any(
            ns != '' and simple_namespace.startswith(ns)
            for ns in include_only_ns
        )
        # Test if isn't used "\0" flag
        # use "foo\0" to add urls just from "foo" not from subns "foo:bar"
        in_on_null = simple_namespace + '\0' in include_only_ns
        include_namespace = in_on_empty_ns or in_on_is_in_list or in_on_null
    else:
        # by default include this namespace
        include_namespace = True

    if include_namespace:
        for url_name in urlresolver.reverse_dict.keys():
            if isinstance(url_name, str):
                url_patterns = [
                    [f'{namespace_path}{pat[0]}', pat[1]]
                    for pattern in urlresolver.reverse_dict.getlist(url_name)
                    for pat in pattern[0]
                ]
                yield [namespace + url_name, url_patterns]

    # check for inner namespaces
    for inner_ns, (inner_ns_path, inner_urlresolver) in urlresolver.namespace_dict.items():
        inner_ns_path = f'{namespace_path}{inner_ns_path}'
        inner_ns = f'{namespace}{inner_ns}:'

        # if we have inner_ns_path, reconstruct a new resolver so that we can
        # handle regex substitutions within the regex of a namespace.
        if inner_ns_path:
            inner_urlresolver = get_ns_resolver(
                inner_ns_path,
                inner_urlresolver,
                # must turn into tuple because lrucache cannot
                # hash this param otherwise
                tuple(urlresolver.pattern.converters.items())
            )
            inner_ns_path = ''

        # yield values from inner namespaces if any
        for x in prepare_url_list(inner_urlresolver, inner_ns_path, inner_ns):
            yield x


def generate_json(default_urlresolver, script_prefix=None):
    if script_prefix is None:
        script_prefix = get_script_prefix()

    # Ensure consistent ouptut ordering
    urls = sorted(prepare_url_list(default_urlresolver))
    return {
        'urls': [
            [
                force_str(name),
                [
                    [force_str(path), [force_str(arg) for arg in args]]
                    for path, args in patterns
                ],
            ] for name, patterns in urls
        ],
        'prefix': script_prefix,
    }


def _safe_json(obj):
    return mark_safe(
        json
        .dumps(obj)
        # replace potentially harmful values from JSON
        # before marking string as safe
        .replace('>', '\\u003E')
        .replace('<', '\\u003C')
        .replace('&', '\\u0026')
    )


def generate_js(default_urlresolver):
    js_var_name = settings.JS_VAR_NAME
    js_global_object_name = settings.JS_GLOBAL_OBJECT_NAME
    script_prefix = settings.JS_SCRIPT_PREFIX
    if script_prefix and not script_prefix.endswith('/'):
        script_prefix = f'{script_prefix}/'
    elif not script_prefix:
        script_prefix = get_script_prefix()

    data = generate_json(default_urlresolver, script_prefix)
    js_content = loader.render_to_string('django_reverse_js/url-resolver.js', {
        'data': _safe_json(data),
        'js_name': '.'.join([js_global_object_name, js_var_name]),
    })

    return js_content


def generate_cjs_module():
    return loader.render_to_string('django_reverse_js/url-resolver.js', {
        'data': "false",
        'js_name': 'module.exports',
    })
