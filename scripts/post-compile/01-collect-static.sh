#!/usr/bin/env bash
set -eo pipefail

indent() {
    RE="s/^/       /"
    [ $(uname) == "Darwin" ] && sed -l "$RE" || sed -u "$RE"
}

MANAGE_FILE=$(find . -maxdepth 3 -type f -name 'manage.py' | head -1)
MANAGE_FILE=${MANAGE_FILE:2}

echo "-----> Collecting static files"
python $MANAGE_FILE collectstatic --noinput  2>&1 | sed '/^Copying/d;/^$/d;/^ /d' | indent

echo