from decouple import config
from core import plugins


DJANGO_MIDDLEWARES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

THIRD_PARTY = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

WIKILEGIS_MIDDLEWARES = [
    # 'wikilegis.core.middleware.ForceLangMiddleware',
]

plugins_dict = plugins.load_current_plugins()

for name, is_active in plugins_dict.items():
    if is_active:
        plugin_settings = plugins.get_settings(name)
        WIKILEGIS_MIDDLEWARES += plugin_settings.MIDDLEWARE_CLASSES

if config('ENABLE_REMOTE_USER', default=0, cast=bool):
    WIKILEGIS_MIDDLEWARES += [
        'wikilegis.auth2.middlewares.WikilegisRemoteUser'
    ]
    DJANGO_MIDDLEWARES.remove(
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware'
    )

MIDDLEWARE = THIRD_PARTY + DJANGO_MIDDLEWARES + WIKILEGIS_MIDDLEWARES
