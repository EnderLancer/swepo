#!/usr/bin/env bash

cd /home/ubuntu/swepo/

# activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

install requirements.txt
pip install -r /home/ubuntu/swepo/requirements.txt

# migrate DB
python app/manage.py migrate