import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)

API_KEY = '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
SECRET_KEY = 'g8#!8*0sr!zsg!q=on=n66dtie69u0z1qhfk-&c8bc_%t#&g@%'

FORCE_SCRIPT_NAME = "/"
SITE_ID = 1

DEBUG = True
ALLOWED_HOSTS = []

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ROOT_URLCONF = 'wikilegis.urls'
INCLUDE_REGISTER_URL = False

WSGI_APPLICATION = 'wikilegis.wsgi.application'

STATIC_IPS = ('127.0.0.1', '::1', )
