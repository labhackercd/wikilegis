FROM labhackercd/python3-nodejs
RUN apt-get update
RUN apt-get install -y bash g++ make python3-dev python3-pip zlib1g-dev libjpeg-dev libgdal-dev libpq-dev libpq5 gettext

RUN mkdir -p /var/labhacker/wikilegis
ADD requirements.txt /var/labhacker/wikilegis
WORKDIR /var/labhacker/wikilegis
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2 gunicorn

ADD . /var/labhacker/wikilegis
RUN npm install
WORKDIR /var/labhacker/wikilegis/wikilegis
