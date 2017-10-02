#!/bin/bash

BASEDIR=$(dirname "$0")
source $BASEDIR/stop-all-containers.sh

sudo docker volume rm $(sudo docker volume ls -q)