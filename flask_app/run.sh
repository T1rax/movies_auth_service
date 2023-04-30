#!/usr/bin/env bash

set -e

# flask db init
#flask db stamp head
#flask db migrate
flask db upgrade

gunicorn --bind 0.0.0.0:5000 wsgi_app:app --workers 3 --log-file=- --access-logfile=- --error-logfile=-