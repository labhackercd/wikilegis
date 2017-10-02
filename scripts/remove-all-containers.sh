#!/bin/bash
BASEDIR=$(dirname "$0")
source $BASEDIR/remove-all-volumes.sh

sudo docker rmi -f $( sudo docker images -q ) # Remove images