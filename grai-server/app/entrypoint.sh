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

# Determine the type of running worker and set the INSTANCE_TYPE environment variable
if [ "$1" = "/start-celerybeat" ]; then
  INSTANCE_TYPE="beat"
elif [ "$1" = "/start-celeryworker" ]; then
  INSTANCE_TYPE="worker"
else
  INSTANCE_TYPE="web"
fi
export INSTANCE_TYPE=$INSTANCE_TYPE

# Run the initialization script if this is a web instance
if [ "$INSTANCE_TYPE" = "web" ]; then
  echo "Initializing database with default data..."
  bash /usr/src/app/initialize_db.sh
fi

exec "$@"
