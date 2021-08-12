import re
from django.conf import settings as _settings
from django.core.exceptions import ImproperlyConfigured


class _JSReverseSettings:
    JS_IDENTIFIER_RE = re.compile(r'^[$A-Z_][\dA-Z_$]*$')

    @property
    def JS_VAR_NAME(self):
        """JS variable name to which assign url-resolver, default :code:`Urls`."""
        var_name = getattr(_settings, 'REVERSEJS_VAR_NAME', 'Urls')
        if not self.JS_IDENTIFIER_RE.match(var_name.upper()):
            raise ImproperlyConfigured(
                f'REVERSEJS_VAR_NAME setting "{var_name}" is not a valid javascript identifier.'
            )
        return var_name

    @property
    def JS_GLOBAL_OBJECT_NAME(self):
        """JS global object to which bound url-resolver, default :code:`this`."""
        global_name = getattr(_settings, 'REVERSEJS_GLOBAL_OBJECT_NAME', 'this')
        if not self.JS_IDENTIFIER_RE.match(global_name.upper()):
            raise ImproperlyConfigured(
                f'REVERSEJS_GLOBAL_OBJECT_NAME setting "{global_name}" is not a valid javascript identifier.'
            )

        return global_name

    @property
    def JS_EXCLUDE_NAMESPACES(self):
        return getattr(_settings, 'REVERSEJS_EXCLUDE_NAMESPACES', [])

    @property
    def JS_INCLUDE_ONLY_NAMESPACES(self):
        return getattr(_settings, 'REVERSEJS_INCLUDE_ONLY_NAMESPACES', [])

    @property
    def JS_SCRIPT_PREFIX(self):
        return getattr(_settings, 'REVERSEJS_SCRIPT_PREFIX', None)


    @property
    def JS_OUTPUT_PATH(self):
        return getattr(_settings, 'REVERSEJS_OUTPUT_PATH', None)


settings = _JSReverseSettings()
