from dj_database_url import parse as db_url
from decouple import config, Csv
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)

API_KEY = config('API_KEY', default='api_key')
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

DATABASES = dict(default=config(
    'DATABASE_URL',
    cast=db_url,
    default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
))

ROOT_URLCONF = 'wikilegis.urls'
INCLUDE_REGISTER_URL = False

WSGI_APPLICATION = 'wikilegis.wsgi.application'

STATIC_IPS = ('127.0.0.1', '::1', )
