from django import template
from django.utils.safestring import mark_safe
from django.urls import get_resolver
from ..core import generate_js


register = template.Library()
urlconf = template.Variable('request.urlconf')


def _get_urlconf(context):
    try:
        return context.request.urlconf
    except AttributeError:
        pass
    try:
        return urlconf.resolve(context)
    except template.VariableDoesNotExist:
        pass


@register.simple_tag(takes_context=True)
def reverse_js(context):
    """
    Outputs a string of JavaScript that can generate URLs via the use
    of the names given to those URLs.
    """
    return mark_safe(generate_js(get_resolver(_get_urlconf(context))))
