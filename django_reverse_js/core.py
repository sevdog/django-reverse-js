import json
from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.utils.safestring import mark_safe
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
        include_namespace = (
            # urls without namespace
            (not namespace and '' in include_only_ns)
            # check that "\0" flag isn't used
            # use "foo\0" to add urls just from "foo" not from subns "foo:bar"
            or f'{simple_namespace}\0' in include_only_ns
            # check if nestead ns isn't subns of include_only ns
            # e.g. ns = "foo:bar" include_only = ["foo"] -> this ns will be used
            # works for ns = "lorem:ipsum:dolor" include_only = ["lorem:ipsum"]
            # ns "lorem" will be ignored but "lorem:ipsum" & "lorem:ipsum:.." won't
            or any(ns and simple_namespace.startswith(ns) for ns in include_only_ns)
        )
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
                yield namespace + url_name, url_patterns

    # check for inner namespaces
    for inner_ns, (
        inner_ns_path,
        inner_urlresolver,
    ) in urlresolver.namespace_dict.items():
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
                tuple(urlresolver.pattern.converters.items()),
            )
            inner_ns_path = ''

        # yield values from inner namespaces if any
        yield from prepare_url_list(inner_urlresolver, inner_ns_path, inner_ns)


def generate_json(default_urlresolver, script_prefix=None):
    if script_prefix is None:
        script_prefix = get_script_prefix()

    # re-arrange structure for JSON
    # use a generator to reduce number of iterations
    urls = (
        [name, [[path, [arg for arg in args]] for path, args in patterns]]
        for name, patterns in prepare_url_list(default_urlresolver)
    )
    return {
        # ensure consistent ouptut ordering
        'urls': sorted(urls),
        'prefix': script_prefix,
    }


_json_script_escapes = {
    ord(">"): "\\u003E",
    ord("<"): "\\u003C",
    ord("&"): "\\u0026",
}


def _safe_json(obj):
    # replace potentially harmful values from JSON
    # before marking string as safe
    return mark_safe(json.dumps(obj).translate(_json_script_escapes))


def generate_js(default_urlresolver):
    script_prefix = settings.JS_SCRIPT_PREFIX or get_script_prefix()
    if not script_prefix.endswith('/'):
        script_prefix = f'{script_prefix}/'

    js_content = loader.render_to_string(
        'django_reverse_js/url-resolver.tpl.js',
        {
            'data': _safe_json(generate_json(default_urlresolver, script_prefix)),
            'js_name': f'{settings.JS_GLOBAL_OBJECT_NAME}.{settings.JS_VAR_NAME}',
            'reversejs_template': settings.JS_TEMPLATE,
        },
    )

    return js_content


def generate_cjs_module():
    return loader.render_to_string(
        'django_reverse_js/url-resolver.tpl.js',
        {
            'data': 'false',
            'js_name': 'module.exports',
            'reversejs_template': settings.JS_TEMPLATE,
        },
    )
