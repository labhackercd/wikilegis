# Requirements

* Python 2.7.x
* Probably a working C compiler and `make` (to build libsass)
* Pillow install dependencies [1]
* libjpeg-dev, zlib1g-dev and build-essential (for debian like distributions)

# Installation

```bash
$ git clone https://github.com/labhackercd/wikilegis.git
$ cd wikilegis
$ npm install
$ pip install -r requirements.txt
```

# Customizing settings

To customize some wikilegis settings, create the file  `settings.ini` on `./wikilegis/settings/`. The availables parameters are:

```
[settings]

# Application settings
API_KEY = api_key
SECRET_KEY = secret_key
FORCE_SCRIPT_NAME
DEBUG = 1 # True
ALLOWED_HOSTS = *
DATABASE_ENGINE = sqlite3 # postgresql, mysql, sqlite3, oracle
DATABASE_NAME = db.sqlite3
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT

# Authentication settings
LOGIN_URL = /accounts/login/
LOGIN_REDIRECT_URL = /
AUTH_USER_MODEL = auth2.User
ENABLE_REMOTE_USER = 0 # False
SESSION_COOKIE_NAME = sessionid
ACCOUNT_ACTIVATION_REQUIRED = 0 # False
ACCOUNT_ACTIVATION_DAYS = 7
ENABLE_SOCIAL_AUTH = 1 # True

# Email settings
EMAIL_HOST = localhost
EMAIL_PORT = 587
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
EMAIL_USE_TLS
DEFAULT_FROM_EMAIL

# Locale settings
LANGUAGE_CODE = pt-br
TIME_ZONE = America/Sao_Paulo

# Logging settings
LOG_DIR = wikilegis.log

# Staticfiles settings
STATIC_URL = /static/
MEDIA_URL = /media/

# Legacy Wikilegis settings
CONNECT_TO_LEGACY_WIKILEGIS = 0 # False
LEGACY_DATABASE_ENGINE = sqlite3 # postgresql, mysql, sqlite3, oracle
LEGACY_DATABASE_NAME = legacy.sqlite3
LEGACY_DATABASE_USER
LEGACY_DATABASE_PASSWORD
LEGACY_DATABASE_HOST
LEGACY_DATABASE_PORT

```

# Plugins

You can list all available plugins with:

```bash
$ ./manage.py list_plugins

Availables plugins:
[ ] camara_deputados
```

If the listed plugin is active, the "checkbox" will be filled with "X". Otherwise, will be empty.

## Activating plugins

Once you have listed all available plugins, you can activate one of them. To do this you have to execute the following django command:

```bash
$ ./manage.py activate_plugin plugin_name
```

After run this command, all plugin dependencies will be installed using `pip`. If you're using `virtualenv`, problably you'll not have problems. But if you're not using, you must run this command with `root` previlleges.

## Deactivating plugins

To deactivate one plugin:

```bash
$ ./manage.py deactivate_plugin plugin_name
```

Note that plugin dependencies will remain installed on your system.

# Database and superuser setup

```bash
$ ./manage.py migrate
$ ./manage.py createsuperuser
```


# Running the development server

```bash
$ ./manage.py runserver
```


# Admin interface

If everything went right, the admin interface is now available at: http://127.0.0.1:8000/admin. You can log in using the superuser credentials you just created and manage all kinds of contents. Once you're done managing your site, go visit the main page at http://127.0.0.1:8000/.


# Translating

TODO: Instructions to use Transifex to translate this.



[1]: https://pillow.readthedocs.org/en/latest/installation.html
