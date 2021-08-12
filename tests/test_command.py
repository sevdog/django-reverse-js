import pathlib
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import SimpleTestCase, override_settings
from django.urls import get_resolver
from django_reverse_js.core import generate_js


PARENT_DIR = pathlib.Path(__file__).parent


class CommandTestCase(SimpleTestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        # clean up static directory
        def rm_tree(path):
            for child in path.glob('*'):
                if child.is_file():
                    child.unlink()
                else:
                    rm_tree(child)

            path.rmdir()

        test_path = PARENT_DIR / 'django_reverse_js'
        if test_path.exists():
            rm_tree(test_path)

    def test_reverse_js_file_save(self):
        call_command('createstatic_reversejs')
        default_file_path = pathlib.Path(settings.STATIC_ROOT) / 'django_reverse_js' / 'js' / 'reverse.js'
        with default_file_path.open() as js_file:
            produced_file = js_file.read()

        expected_js = generate_js(get_resolver())
        self.assertEqual(expected_js, produced_file)

    @override_settings(STATIC_ROOT=None)
    def test_missing_static_root(self):
        with self.assertRaises(ImproperlyConfigured):
            call_command('createstatic_reversejs')

    @override_settings(
        STATIC_ROOT=None,
        # point to same dir with a different name
        REVERSEJS_OUTPUT_PATH=PARENT_DIR / 'django_reverse_js'
    )
    def test_output_path(self):
        call_command('createstatic_reversejs')
        default_file_path = PARENT_DIR / 'django_reverse_js' / 'reverse.js'
        with default_file_path.open() as js_file:
            produced_file = js_file.read()

        expected_js = generate_js(get_resolver())
        self.assertEqual(expected_js, produced_file)
