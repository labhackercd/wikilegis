#!/usr/bin/env python
from django.core import management
import django
import os
import random
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wikilegis.settings.wikilegis")
django.setup()


def create_key_file(filename, key):
    if os.path.exists(filename):
        secret_file = open(filename, 'r')
        key = secret_file.read()
        secret_file.close()
    else:
        secret_file = open(filename, 'w')
        secret_file.write(key)
        secret_file.close()
    return key


def create_secret_keys():
    secret = create_key_file(os.path.join(BASE_DIR, '../secret.key'),
                             '%030x' % random.randrange(16 ** 64))
    api = create_key_file(os.path.join(BASE_DIR, '../api.key'),
                          '%030x' % random.randrange(16 ** 64))
    return secret, api


def create_settings_ini(settings):
    settings_path = os.path.join(BASE_DIR, './wikilegis/settings/settings.ini')
    print(BASE_DIR, '/wikilegis/settings/settings.ini')
    if os.path.exists(settings_path):
        open(settings_path, 'w').close()

    settings_file = open(settings_path, 'w')
    settings_lines = ['[settings]\n']
    for key, value in settings.items():
        if value:
            settings_lines.append('{} = {}\n'.format(key, value))
    settings_file.writelines(settings_lines)
    settings_file.close()


def create_admin():
    from accounts.models import User

    password = os.environ.get('ADMIN_PASSWORD')
    email = os.environ.get('ADMIN_EMAIL')
    if not email:
        print("Environment variable $ADMIN_EMAIL was not set.")
        sys.exit('MISSING_ADMIN_EMAIL')
    if User.objects.filter(email=email).exists():
        print("Admin already exists. Exiting without change.")
        sys.exit(0)
    else:
        if not password:
            print("Environment variable $ADMIN_PASSWORD was not set.")
            sys.exit('MISSING_ADMIN_PASSWORD')
        user = User.objects.create_superuser(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()


if __name__ == '__main__':
    settings = {}
    settings['SECRET_KEY'], settings['API_KEY'] = create_secret_keys()
    settings['FORCE_SCRIPT_NAME'] = os.environ.get('FORCE_SCRIPT_NAME')
    variables = [
        'DEBUG', 'ALLOWED_HOSTS', 'DATABASE_ENGINE', 'DATABASE_NAME',
        'DATABASE_USER', 'DATABASE_PASSWORD', 'DATABASE_HOST', 'DATABASE_PORT',
        'LOGIN_URL', 'LOGIN_REDIRECT_URL', 'AUTH_USER_MODEL',
        'ENABLE_REMOTE_USER', 'SESSION_COOKIE_NAME',
        'ACCOUNT_ACTIVATION_REQUIRED', 'ACCOUNT_ACTIVATION_DAYS',
        'ENABLE_SOCIAL_AUTH', 'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD', 'EMAIL_USE_TLS', 'DEFAULT_FROM_EMAIL',
        'LANGUAGE_CODE', 'TIME_ZONE', 'LOG_DIR', 'STATIC_URL', 'MEDIA_URL',
        'CONNECT_TO_LEGACY_WIKILEGIS', 'LEGACY_DATABASE_ENGINE',
        'LEGACY_DATABASE_NAME', 'LEGACY_DATABASE_USER',
        'LEGACY_DATABASE_PASSWORD', 'LEGACY_DATABASE_HOST',
        'LEGACY_DATABASE_PORT'
    ]

    for variable in variables:
        settings[variable] = os.environ.get(variable)

    create_settings_ini(settings)
    management.call_command('migrate')
    create_admin()
