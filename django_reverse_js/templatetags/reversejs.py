from contextlib import suppress
from django import template
from django.utils.safestring import SafeString, mark_safe
from django.urls import get_resolver
from ..core import generate_js


register = template.Library()
urlconf = template.Variable('request.urlconf')


def _get_urlconf(context: template.Context) -> str | None:
    with suppress(AttributeError):
        return context.request.urlconf  # type: ignore[attr-defined]

    with suppress(template.VariableDoesNotExist):
        return urlconf.resolve(context)

    return None


@register.simple_tag(takes_context=True)
def reverse_js(context: template.Context) -> SafeString:
    """
    Outputs a string of JavaScript that can generate URLs via the use
    of the names given to those URLs.
    """
    return mark_safe(generate_js(get_resolver(_get_urlconf(context))))
