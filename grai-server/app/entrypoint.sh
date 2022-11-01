#!/bin/sh -x

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do sleep 1; done
echo "PostgreSQL started"


#python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py shell < "superuser_init.py"

exec "$@"
