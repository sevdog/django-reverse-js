from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, override_settings
from django_reverse_js.conf import settings


class SettingsTestCase(SimpleTestCase):
    def test_invalid_varname(self):
        with override_settings(REVERSEJS_VAR_NAME='1test'):
            with self.assertRaisesMessage(
                ImproperlyConfigured, '"1test" is not a valid javascript identifier'
            ):
                settings.JS_VAR_NAME

        with override_settings(REVERSEJS_VAR_NAME='?test'):
            with self.assertRaisesMessage(
                ImproperlyConfigured, '"?test" is not a valid javascript identifier'
            ):
                settings.JS_VAR_NAME

        with override_settings(REVERSEJS_VAR_NAME='*test'):
            with self.assertRaisesMessage(
                ImproperlyConfigured, '"*test" is not a valid javascript identifier'
            ):
                settings.JS_VAR_NAME

    def test_invalid_globalname(self):
        with override_settings(REVERSEJS_GLOBAL_OBJECT_NAME='1test'):
            with self.assertRaisesMessage(
                ImproperlyConfigured, '"1test" is not a valid javascript identifier'
            ):
                settings.JS_GLOBAL_OBJECT_NAME

        with override_settings(REVERSEJS_GLOBAL_OBJECT_NAME='?test'):
            with self.assertRaisesMessage(
                ImproperlyConfigured, '"?test" is not a valid javascript identifier'
            ):
                settings.JS_GLOBAL_OBJECT_NAME

        with override_settings(REVERSEJS_GLOBAL_OBJECT_NAME='*test'):
            with self.assertRaisesMessage(
                ImproperlyConfigured, '"*test" is not a valid javascript identifier'
            ):
                settings.JS_GLOBAL_OBJECT_NAME
