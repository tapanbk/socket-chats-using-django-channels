#!/bin/sh
echo "=======Waiting for postgres...======="
python manage.py collectstatic --no-input

until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "=======Waiting for PostgreSQL to become available...======="
  sleep 2
done
echo "=======PostgreSQL is ready=========================="
python manage.py flush --no-input
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
python manage.py test