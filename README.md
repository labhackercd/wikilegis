# Requirements

* Python 2.7.x
* Probably a working C compiler and `make` (to build libsass)
* Pillow install dependencies [1]
* libjpeg-dev, zlib1g-dev and build-essential (for debian like distributions)

# Installation

```bash
$ git clone https://github.com/labhackercd/wikilegis.git
$ cd wikilegis
$ pip install -r requirements.txt
```


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
