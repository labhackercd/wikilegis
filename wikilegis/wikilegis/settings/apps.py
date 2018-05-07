from decouple import config
from core import plugins


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
    'constance',
    'constance.backends.database',
    'compressor',
    'compressor_toolkit',
    'debug_toolbar',
    'tastypie',
    'corsheaders',
    'djangobower',
    'crispy_forms',
    'embed_video',
]

if config('ENABLE_SOCIAL_AUTH', default=0, cast=bool):
    THIRD_PARTY.append('social_django')

WIKILEGIS_APPS = [
    'accounts',
    'core',
    'api',
    'notification',
]

plugins_dict = plugins.load_current_plugins()

for name, is_active in plugins_dict.items():
    if is_active:
        plugin_settings = plugins.get_settings(name)
        plugin_apps = getattr(plugin_settings, 'INSTALLED_APPS', [])
        THIRD_PARTY += plugin_apps
        WIKILEGIS_APPS.insert(0, 'plugins.' + name)

if config('CONNECT_TO_LEGACY_WIKILEGIS', default=False, cast=bool):
    WIKILEGIS_APPS.append('legacy')

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + WIKILEGIS_APPS
