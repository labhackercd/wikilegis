#!/bin/bash
WIKILEGIS_DIR="/var/labhacker/wikilegis"

python config.py
python manage.py bower_install --allow-root
python manage.py compress --force
python manage.py collectstatic --no-input
python manage.py compilemessages

NAME="Wikilegis"
DJANGODIR=/var/labhacker/wikilegis/wikilegis/
USER=`whoami`
GROUP=`whoami`
NUM_WORKERS=9
DJANGO_WSGI_MODULE=wikilegis.wsgi

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=0.0.0.0:8000
