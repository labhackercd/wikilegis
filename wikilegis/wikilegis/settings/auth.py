from decouple import config
from . import application


LOGIN_URL = config('LOGIN_URL', default='/accounts/login/')
LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', default='/')

AUTH_USER_MODEL = config('AUTH_USER_MODEL', default='auth.User')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

if config('ENABLE_REMOTE_USER', default=0, cast=bool):
    AUTHENTICATION_BACKENDS = (
        'wikilegis.auth2.backends.WikielgisAuthBackend',
    )
else:
    AUTHENTICATION_BACKENDS = (
        'social_core.backends.google.GoogleOAuth2',
        'social_core.backends.facebook.FacebookOAuth2',
        'rules.permissions.ObjectPermissionBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME', default='sessionid')

ACCOUNT_ACTIVATION_REQUIRED = config('ACCOUNT_ACTIVATION_REQUIRED', cast=bool,
                                     default=(not application.DEBUG))
ACCOUNT_ACTIVATION_DAYS = config('ACCOUNT_ACTIVATION_DAYS', default=7,
                                 cast=int)

REGISTRATION_AUTO_LOGIN = True
REGISTRATION_FORM = 'wikilegis.auth2.forms.RegistrationForm'
REGISTRATION_EMAIL_SUBJECT_PREFIX = ""
