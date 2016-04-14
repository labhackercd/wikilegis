[![Travis-ci Build Status](https://travis-ci.org/wikimedia/mediawiki.svg?branch=master)](https://travis-ci.org/mbonaci/mbo-storm)

# Wikilegis

Wikilegis is a project developed in Python by the Brazilian Chamber of Deputies’ Hacker Lab, designed to enable citizens to suggest modifications to the wording of Bills.

Visit our website [Wikilegis](http://wikilegis.labhackercd.net).

# Requirements

* Python 2.7.x
* Probably a working C compiler and `make` (to build libsass).
* Pillow install dependencies. Install [here](https://pillow.readthedocs.org/en/latest/installation.html).
* Virtualenv (Recommended for OS X users). Install [here](http://sourabhbajaj.com/mac-setup/Python/virtualenv.html).

# Installation

Clone the repository:
```bash
  $ git clone https://github.com/labhackercd/wikilegis.git
```

Enter in the project directory:
```bash
  $ cd wikilegis
```

Install all the project dependencies:
```bash
  $ pip install -r requirements.txt
```


# Database and superuser setup

```bash
  $ ./manage.py migrate
```
```bash
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
