from pathlib import Path
from django.conf import settings as dj_settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand
from django.urls import get_resolver
from ...core import generate_js
from ...conf import settings


class Command(BaseCommand):
    help = 'Creates a static urls-js file for django-reverse-js'
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            'out_file', type=Path, nargs='?',
            help='Output file name', default=Path('reverse.js')
        )

    def get_location(self):
        output_path = settings.JS_OUTPUT_PATH
        if output_path:
            return Path(output_path)

        if not hasattr(dj_settings, 'STATIC_ROOT') or not dj_settings.STATIC_ROOT:
            raise ImproperlyConfigured(
                'The collectstatic_js_reverse command needs '
                'settings.REVERSEJS_OUTPUT_PATH or settings.STATIC_ROOT to be set.'
            )

        return Path(dj_settings.STATIC_ROOT) / 'django_reverse_js' / 'js'

    def handle(self, *args, **options):
        out_filename = str(options.get('out_file'))
        verbosity = options.get('verbosity')
        location = self.get_location()
        fs = FileSystemStorage(location=location)
        # remove file if it was already present
        if fs.exists(out_filename):
            fs.delete(out_filename)

        default_urlresolver = get_resolver()
        content = generate_js(default_urlresolver)
        fs.save(out_filename, ContentFile(content))
        if verbosity > 0:
            self.stdout.write(f'js-reverse file written to {location}')
