from decouple import config, Csv
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = config('SECRET_KEY', default='secret_key')

FORCE_SCRIPT_NAME = config('FORCE_SCRIPT_NAME', default=None)
SITE_ID = 1

DEBUG = config('DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = config('ALLOWED_HOSTS',
                       cast=Csv(lambda x: x.strip().strip(',').strip()),
                       default='*')


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS'
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + config('DATABASE_ENGINE',
                                                 default='sqlite3'),
        'NAME': config('DATABASE_NAME', default='db.sqlite3'),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}

if config('CONNECT_TO_LEGACY_WIKILEGIS', default=False, cast=bool):
    DATABASES['legacy'] = {
        'ENGINE': 'django.db.backends.' + config('LEGACY_DATABASE_ENGINE',
                                                 default='sqlite3'),
        'NAME': config('LEGACY_DATABASE_NAME', default='legacy.sqlite3'),
        'USER': config('LEGACY_DATABASE_USER', default=''),
        'PASSWORD': config('LEGACY_DATABASE_PASSWORD', default=''),
        'HOST': config('LEGACY_DATABASE_HOST', default=''),
        'PORT': config('LEGACY_DATABASE_PORT', default=''),
    }

ROOT_URLCONF = 'wikilegis.urls'
INCLUDE_REGISTER_URL = False

WSGI_APPLICATION = 'wikilegis.wsgi.application'

STATIC_IPS = ('127.0.0.1', '::1', )
