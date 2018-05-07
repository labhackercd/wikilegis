from decouple import config
import django.conf.global_settings as default
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)

NODE_MODULES = os.path.join(os.path.dirname(BASE_DIR), 'node_modules')

STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public'))

STATICFILES_FINDERS = [
    'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
] + default.STATICFILES_FINDERS

STATICFILES_DIRS = [
    NODE_MODULES,
    os.path.abspath(os.path.join(BASE_DIR, 'static'))
]

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')
BOWER_PATH = os.path.join(NODE_MODULES, '.bin/bower')
BOWER_INSTALLED_APPS = [
    'normalize.css#5.0.0',
    'https://github.com/labhackercd/fontastic-labhacker.git',
]

COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
    ('module', 'compressor_toolkit.precompilers.ES6Compiler'),
]

COMPRESS_NODE_MODULES = NODE_MODULES
COMPRESS_NODE_SASS_BIN = os.path.join(NODE_MODULES, '.bin/node-sass')
COMPRESS_POSTCSS_BIN = os.path.join(NODE_MODULES, '.bin/postcss')
COMPRESS_BROWSERIFY_BIN = os.path.join(NODE_MODULES, '.bin/browserify')
COMPRESS_SCSS_COMPILER_CMD = '{node_sass_bin}' \
                             ' --source-map true' \
                             ' --source-map-embed true' \
                             ' --source-map-contents true' \
                             ' --output-style expanded' \
                             ' {paths} "{infile}" "{outfile}"' \
                             ' &&' \
                             ' {postcss_bin}' \
                             ' --use "{node_modules}/autoprefixer"' \
                             ' --autoprefixer.browsers' \
                             ' "{autoprefixer_browsers}"' \
                             ' -r "{outfile}"'
COMPRESS_OFFLINE = config('COMPRESS_OFFLINE', default=False)

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
    'constance.context_processors.config',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
]
