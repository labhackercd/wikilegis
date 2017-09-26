#!/bin/bash
WIKILEGIS_DIR="/var/labhacker/wikilegis"

python3 manage.py migrate

NAME="Wikilegis"
[[ -z "${WORKERS}" ]] && NUM_WORKERS=2 || NUM_WORKERS="${WORKERS}"
DJANGO_WSGI_MODULE=wikilegis.wsgi

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=0.0.0.0:8000
