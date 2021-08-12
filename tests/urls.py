from copy import deepcopy
from django.views.generic import View
from django.urls import path, re_path, include
from django_reverse_js.views import urls_js


dummy_view = View.as_view()

basic_patterns = [
    # test urls
    path('test_no_url_args', dummy_view, name='test_no_url_args'),
    path('test_script', dummy_view, name='</script><script>console.log(&amp;)</script><!--'),
    path('test_one_url_args/<str:arg_one>', dummy_view, name='test_one_url_args'),
    path('test_two_url_args/<str:arg_one>-<str:arg_two>', dummy_view, name='test_two_url_args'),
    re_path(r'^test_optional_url_arg/(?:1_(?P<arg_one>[-\w]+)-)?2_(?P<arg_two>[-\w]+)/$', dummy_view, name='test_optional_url_arg'),
    path('test_duplicate_name/<str:arg_one>', dummy_view, name='test_duplicate_name'),
    path('test_duplicate_name/<str:arg_one>-<str:arg_two>', dummy_view, name='test_duplicate_name'),
    re_path(r'^test_duplicate_argcount/(?P<arg_one>[-\w]+)?-(?P<arg_two>[-\w]+)?/$', dummy_view, name='test_duplicate_argcount'),
]

urlpatterns = deepcopy(basic_patterns)

# test exclude namespaces urls
urlexclude = [
    path('test_exclude_namespace', dummy_view, name='test_exclude_namespace_url1'),
]


# test namespace
pattern_ns_1 = [
    path('', include(basic_patterns)),
]

pattern_ns_2 = [
    path('', include(basic_patterns)),
]

pattern_ns = [
    path('', include(basic_patterns)),
]

pattern_nested_ns = [
    path('ns1/', include((pattern_ns_1, 'ns1'), namespace='ns1')),
]

pattern_dubble_nested2_ns = [
    path('ns1/', include((pattern_ns_1, 'ns1'), namespace='ns1')),
]

pattern_dubble_nested_ns = [
    path('ns1/', include((pattern_ns_1, 'ns1'), namespace='ns1')),
    path('nsdn2/', include((pattern_dubble_nested2_ns, 'nsdn2'), namespace='nsdn2')),
]

pattern_only_nested_ns = [
    path('ns1/', include(pattern_ns_1)),
    path('nsdn0/', include((pattern_dubble_nested2_ns, 'nsdn0'), namespace='nsdn0')),
]

urlpatterns += [
    path('ns1/', include((pattern_ns_1, 'ns1'), namespace='ns1')),
    path('ns2/', include((pattern_ns_2, 'ns2'), namespace='ns2')),
    path('ns_ex/', include((urlexclude, 'exclude_namespace'), namespace='exclude_namespace')),
    path('ns<path:ns_arg>/', include((pattern_ns, 'ns_arg'), namespace='ns_arg')),
    path('nestedns/', include((pattern_nested_ns, 'nestedns'), namespace='nestedns')),
    path('nsdn/', include((pattern_dubble_nested_ns, 'nsdn'), namespace='nsdn')),
    path('nsno/', include((pattern_only_nested_ns, 'nsno'), namespace='nsno')),
    path('jsreverse', urls_js, name='js_reverse'),
]
