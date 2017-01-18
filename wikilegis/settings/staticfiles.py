from easy_thumbnails.conf import Settings as thumbnail_settings
from decouple import config
from . import application
import django.conf.global_settings as default
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS


STATIC_URL = config('STATIC_URL', default='/static/')

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public', 'static'))

STATICFILES_FINDERS = default.STATICFILES_FINDERS + [
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'wikilegis', 'static'),
]

COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'django_libsass.SassCompiler'),
]

LIBSASS_SOURCEMAPS = application.DEBUG

MEDIA_URL = config('MEDIA_URL', default='/media/')

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public', 'media'))

DJANGO_CONTEXT_PROCESSORS = [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.template.context_processors.media',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]

THIRD_PARTY_CONTEXT_PROCESSORS = [
    'social_django.context_processors.backends',
    'social_django.context_processors.login_redirect',
]

WIKILEGIS_CONTEXT_PROCESSORS = [
]

CONTEXT_PROCESSORS = DJANGO_CONTEXT_PROCESSORS + THIRD_PARTY_CONTEXT_PROCESSORS
CONTEXT_PROCESSORS += WIKILEGIS_CONTEXT_PROCESSORS


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'wikilegis', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
]
