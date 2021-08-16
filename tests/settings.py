# assert warnings are enabled
import warnings
import pathlib


warnings.simplefilter("ignore", Warning)
BASE_DIR = pathlib.Path(__file__).parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

INSTALLED_APPS = [
    "django_reverse_js",
    "tests",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

ROOT_URLCONF = 'tests.urls'
SECRET_KEY = "foobar"
STATIC_ROOT = BASE_DIR
