#!/bin/bash

echo "Apply Database migrations"
python manage.py makemigrations --noinput
python manage.py migrate

echo "Running Fueled project server"

python manage.py runserver 0.0.0.0:8000
