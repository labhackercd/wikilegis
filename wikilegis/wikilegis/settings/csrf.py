from decouple import config, Csv

CSRF_COOKIE_DOMAIN = config('CSRF_COOKIE_DOMAIN', default=None)
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default=False, cast=bool)
CSRF_COOKIE_NAME = config('CSRF_COOKIE_NAME', default='csrftoken')
CSRF_COOKIE_PATH = config('CSRF_COOKIE_PATH', default='/')
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
CSRF_USE_SESSIONS = config('CSRF_USE_SESSIONS', default=False, cast=bool)
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS',
                              cast=Csv(lambda x: x.strip().strip(',').strip()),
                              default='')
