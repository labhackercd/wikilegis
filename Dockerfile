FROM labhackercd/alpine-python3-nodejs

ENV BUILD_PACKAGES postgresql-dev postgresql-client jpeg-dev \
    zlib-dev gettext

RUN apk add --update --no-cache $BUILD_PACKAGES
RUN mkdir -p /var/labhacker/wikilegis

ADD ./config/etc/cron.d/wikilegis /etc/cron.d/wikilegis
RUN chmod 0644 /etc/cron.d/wikilegis

ADD . /var/labhacker/wikilegis
WORKDIR /var/labhacker/wikilegis

RUN pip3 install -r requirements.txt psycopg2 gunicorn && \
    rm -r /root/.cache

RUN npm install

WORKDIR /var/labhacker/wikilegis/wikilegis
RUN python3 manage.py bower_install --allow-root && \
    python3 manage.py compress --force && \
    python3 manage.py collectstatic --no-input && \
    python3 manage.py compilemessages

EXPOSE 8000
CMD ./start.sh
