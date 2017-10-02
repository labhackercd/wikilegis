#!/bin/bash
sudo docker stop $(sudo docker ps -a -q) # Stop containers
sudo docker rm $(sudo docker ps -a -q) # Remove containers