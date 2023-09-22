#!/bin/sh
#echo "Waiting for postgres..."
#
#while ! nc -z $DB_HOST $DB_PORT; do
#  echo $DB_HOST $DB_PORT
#  sleep 0.1
#  echo "Got lost in this process"
#done
#echo "PostgreSQL started"

python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input

python manage.py runserver 0.0.0.0:8000
