#!/bin/bash

host="${DB_HOST:-localhost}"
port="${DB_PORT:-5432}"

echo "Waiting for postgres..."
while ! nc -z $host $port; do sleep 1; done
echo "PostgreSQL started"

export GRAI_SERVER_VERSION=$(cat /version.txt)
echo "SERVER VERSION: $GRAI_SERVER_VERSION"

# Generate a default random key
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(cat /dev/urandom | env LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
    export SECRET_KEY=$SECRET_KEY
fi

# Run the initialization script if this is a web instance

if [ "$INSTANCE_TYPE" = "server" ]; then
  echo "Initializing database with default data..."
  bash /usr/src/app/initialize_db.sh

  echo "Building retake index..."
  python manage.py build_search
fi

exec "$@"
