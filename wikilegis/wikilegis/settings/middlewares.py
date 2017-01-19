from decouple import config


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

if config('ENABLE_REMOTE_USER', default=0, cast=bool):
    WIKILEGIS_MIDDLEWARES += [
        'wikilegis.auth2.middlewares.WikilegisRemoteUser'
    ]
    DJANGO_MIDDLEWARES.remove(
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware'
    )

MIDDLEWARE = THIRD_PARTY + DJANGO_MIDDLEWARES + WIKILEGIS_MIDDLEWARES
