from django.views.generic import View
from django.template import Context, RequestContext, Template
from django.test import SimpleTestCase, override_settings, RequestFactory
from django.urls import path
from django.utils.encoding import smart_str
from django_reverse_js.templatetags.reversejs import reverse_js
from django_reverse_js.views import urls_js


urlpatterns = [
    path('test_template', View.as_view(), name='test_template_name'),
]


@override_settings(
    TEMPLATE_CONTEXT_PROCESSORS=['django.core.context_processors.request'],
    ROOT_URLCONF=__name__
)
class TemplateTagTest(SimpleTestCase):
    def test_template_tag_with_request_in_context(self):
        request = RequestFactory().get('/')
        request.urlconf = __name__
        template = Template('{% load reversejs %}{% reverse_js %}')
        js = template.render(RequestContext(request))
        self.assertIn('[["test_template_name", [["test_template", []]]]]', js)

    def test_template_tag_with_dict_request_in_context(self):
        request = {'urlconf': __name__}
        template = Template('{% load reversejs %}{% reverse_js %}')
        js = template.render(Context({'request': request}))
        self.assertIn('[["test_template_name", [["test_template", []]]]]', js)

    def test_template_tag_without_request_in_context(self):
        js_from_tag = reverse_js(Context())
        js_from_view = smart_str(urls_js(RequestFactory().get('/')).content)
        self.assertEqual(js_from_tag, js_from_view)

    def test_template_tag_escape_entities(self):
        request = {'urlconf': 'tests.urls'}
        template = Template('{% load reversejs %}{% reverse_js %}')
        js = template.render(Context({'request': request}))
        self.assertIn(
            '\\u003C/script\\u003E\\u003Cscript\\u003Econsole.log(\\u0026amp;)'
            '\\u003C/script\\u003E\\u003C!--',
            js,
        )
