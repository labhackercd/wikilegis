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
    'flat',
    'object_tools',
    'export',
    'haystack',
    'compressor',
    'adminsortable2',
    'debug_toolbar',
    'registration',
    'django_comments',
    'django_extensions',
    'rules.apps.AutodiscoverRulesConfig',
    'embed_video',
    'social.apps.django_app.default',
    'easy_thumbnails',
    'image_cropping',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'crispy_forms',
]

WIKILEGIS_APPS = [
    'wikilegis.auth2',
    'wikilegis.core',
    'wikilegis.comments2',
    'wikilegis.notification',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + WIKILEGIS_APPS
