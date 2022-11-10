#!/bin/sh -x


host="${DB_HOST:-localhost}"
port="${DB_PORT:-5432}"

echo "Waiting for postgres..."
while ! nc -z $host $port; do sleep 1; done
echo "PostgreSQL started"


#python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py shell < "superuser_init.py"

exec "$@"
