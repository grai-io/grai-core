#!/bin/bash


host="${DB_HOST:-localhost}"
port="${DB_PORT:-5432}"

echo "Waiting for postgres..."
while ! nc -z $host $port; do sleep 1; done
echo "PostgreSQL started"

# Set the current package version as an environment variable
export GRAI_SERVER_VERSION=`poetry version -s`

# Generate a default random key
DEFAULT_KEY=`cat /dev/urandom | env LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1`
export SECRET_KEY=${SECRET_KEY:-$DEFAULT_KEY}


#python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input

# Every call to manage.py imports telemetry/apps which have a log event but we only want the first.
export BEGIN_LOGGING="True"
python manage.py shell < "init.py"

# Seed database from json files
python manage.py loaddata connectors

exec "$@"
