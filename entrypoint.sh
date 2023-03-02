#!/bin/bash

echo "Checking database availability"
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

echo "Makemigrations"
python manage.py makemigrations --no-input

echo "Migrate"
python manage.py migrate --no-input

echo "Create super user"
python manage.py custom_create_superuser --no-input

echo "Run gunicorn"
gunicorn --bind 0.0.0.0:8000 --workers 1 core.wsgi:application

exec "$@"