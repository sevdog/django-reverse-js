from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.urls import get_resolver
from .core import generate_js, generate_json

__all__ = ('urls_js', 'urls_json')


@require_GET
def urls_js(request):
    default_urlresolver = get_resolver(getattr(request, 'urlconf', None))
    js_content = generate_js(default_urlresolver)
    return HttpResponse(js_content, content_type='application/javascript')


@require_GET
def urls_json(request):
    default_urlresolver = get_resolver(getattr(request, 'urlconf', None))
    json_data = generate_json(default_urlresolver)
    return JsonResponse(json_data)
