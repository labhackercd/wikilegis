from decouple import config


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
]

THIRD_PARTY = [
    'compressor',
    'compressor_toolkit',
    'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djangobower',
    'crispy_forms',
]

if config('ENABLE_SOCIAL_AUTH', default=0, cast=bool):
    THIRD_PARTY.append('social_django')

WIKILEGIS_APPS = [
    'accounts',
    'core',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + WIKILEGIS_APPS
