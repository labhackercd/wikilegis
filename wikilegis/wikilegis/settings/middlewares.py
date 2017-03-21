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
    'core.middleware.force_default_language_middleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

THIRD_PARTY = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

WIKILEGIS_MIDDLEWARES = [
]

plugins_dict = plugins.load_current_plugins()

for name, is_active in plugins_dict.items():
    if is_active:
        plugin_settings = plugins.get_settings(name)
        pluging_middleware = getattr(plugin_settings, 'MIDDLEWARE_CLASSES', [])
        WIKILEGIS_MIDDLEWARES += pluging_middleware

if config('ENABLE_REMOTE_USER', default=0, cast=bool):
    WIKILEGIS_MIDDLEWARES += [
        'accounts.middlewares.WikilegisRemoteUser'
    ]
    DJANGO_MIDDLEWARES.remove(
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware'
    )

MIDDLEWARE = THIRD_PARTY + DJANGO_MIDDLEWARES + WIKILEGIS_MIDDLEWARES
