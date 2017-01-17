from . import application


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'auth2.User'

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.Facebook2OAuth2',
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ACCOUNT_ACTIVATION_REQUIRED = not application.DEBUG
ACCOUNT_ACTIVATION_DAYS = 7

REGISTRATION_AUTO_LOGIN = True
REGISTRATION_FORM = 'wikilegis.auth2.forms.RegistrationForm'
REGISTRATION_EMAIL_SUBJECT_PREFIX = ""
