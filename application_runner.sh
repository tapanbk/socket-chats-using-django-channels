#!/bin/sh
echo "Waiting for postgres..."

until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "Waiting for PostgreSQL to become available..."
  sleep 2
done
echo "PostgreSQL is ready."

#while ! nc -z $DB_HOST $DB_PORT; do
#  echo $DB_HOST $DB_PORT
#  sleep 10
#  echo "Got lost in this process"
#done
echo "=======PostgreSQL started=========================="

python manage.py flush --no-input
python manage.py migrate
python manage.py test
python manage.py collectstatic --no-input

python manage.py runserver 0.0.0.0:8000
