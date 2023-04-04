import pathlib
import json
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, override_settings
from django.urls import get_resolver
from django_reverse_js.core import prepare_url_list, generate_json


class CoreTestCase(SimpleTestCase):
    def test_full_extraction(self):
        extracted_paths = list(prepare_url_list(get_resolver()))
        self.assertEqual(len(extracted_paths), 65)

    @override_settings(REVERSEJS_EXCLUDE_NAMESPACES=['exclude_namespace'])
    def test_namespace_not_in_response(self):
        extracted_paths = list(prepare_url_list(get_resolver()))
        self.assertEqual(len(extracted_paths), 64)
        self.assertFalse(
            any(url[0].startswith('exclude_namespace:') for url in extracted_paths)
        )

    @override_settings(REVERSEJS_INCLUDE_ONLY_NAMESPACES=['ns1'])
    def test_only_namespace_in_response(self):
        extracted_paths = list(prepare_url_list(get_resolver()))
        self.assertEqual(len(extracted_paths), 7)
        self.assertTrue(all(url[0].startswith('ns1:') for url in extracted_paths))
        self.assertFalse(any(url[0].startswith('ns2:') for url in extracted_paths))
        self.assertFalse(any(url[0].startswith('ns_arg:') for url in extracted_paths))
        self.assertFalse(
            any(url[0].startswith('nesteadns:') for url in extracted_paths)
        )
        self.assertFalse(
            any(url[0].startswith('exclude_namespace:') for url in extracted_paths)
        )
        self.assertFalse(any(url[0].startswith('nsdn:') for url in extracted_paths))
        self.assertFalse(any(url[0].startswith('nsno:') for url in extracted_paths))

    @override_settings(REVERSEJS_INCLUDE_ONLY_NAMESPACES=['nsdn:nsdn'])
    def test_only_namespace_nestead_in_response(self):
        extracted_paths = list(prepare_url_list(get_resolver()))
        self.assertEqual(len(extracted_paths), 7)
        self.assertTrue(all(url[0].startswith('nsdn:nsdn') for url in extracted_paths))
        self.assertTrue(
            any(url[0].startswith('nsdn:nsdn2:ns1') for url in extracted_paths)
        )
        self.assertFalse(any(url[0].startswith('nsdn:ns1') for url in extracted_paths))

    @override_settings(REVERSEJS_INCLUDE_ONLY_NAMESPACES=[''])
    def test_only_empty_namespaces(self):
        extracted_paths = list(prepare_url_list(get_resolver()))
        self.assertEqual(len(extracted_paths), 8)
        # root namespace means to avoid any other inner namespace, so no colon should be in urls
        self.assertFalse(any(':' in url[0] for url in extracted_paths))

    @override_settings(REVERSEJS_INCLUDE_ONLY_NAMESPACES=['nsno\0'])
    def test_only_namespaces_without_subnss(self):
        extracted_paths = list(prepare_url_list(get_resolver()))
        self.assertEqual(len(extracted_paths), 7)
        self.assertTrue(all(url[0].startswith('nsno:') for url in extracted_paths))
        # no inner namespaces should be present
        self.assertFalse(any(':' in url[0][5:] for url in extracted_paths))

    @override_settings(
        REVERSEJS_INCLUDE_ONLY_NAMESPACES=['nsno\0'],
        REVERSEJS_EXCLUDE_NAMESPACES=['exclude_namespace'],
    )
    def test_include_exclude_configuration(self):
        with self.assertRaises(ImproperlyConfigured):
            list(prepare_url_list(get_resolver()))

    def _load_sample_json(self):
        sample_file = pathlib.Path(__file__).parent / 'data' / 'routes.json'
        with sample_file.open() as sf:
            return json.load(sf)

    def test_generate_json(self):
        expected_data = self._load_sample_json()
        json_data = generate_json(get_resolver())
        self.assertEqual(json_data, expected_data)

    def test_generate_json_custom_prerfix(self):
        expected_data = self._load_sample_json()
        json_data = generate_json(get_resolver(), 'thePrefix')
        self.assertEqual(json_data['urls'], expected_data['urls'])
        self.assertEqual(json_data['prefix'], 'thePrefix')
