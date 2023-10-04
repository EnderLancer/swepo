#!/usr/bin/env bash

# kill any servers that may be running in the background 
sudo pkill -f runserver

cd /home/ubuntu/swepo/

# activate virtual environment
source .venv/bin/activate

# run server
screen -d -m python3 app/manage.py runserver 0:8000