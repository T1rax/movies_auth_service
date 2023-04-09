#!/usr/bin/env bash

set -e

gunicorn --bind 0.0.0.0:5000 app:app --workers 3 --log-file=- --access-logfile=- --error-logfile=-