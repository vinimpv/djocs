#!/bin/bash

python src/manage.py migrate --no-input
python src/manage.py collectstatic --no-input
python src/manage.py compress
python src/manage.py runserver 0.0.0.0:8000
