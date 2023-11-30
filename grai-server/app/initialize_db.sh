#!/bin/bash

# Run database migrations
python manage.py migrate

# load fixtures
python manage.py loaddata connectors

# Every call to manage.py imports telemetry/apps which have a log event but we only want the first.
# These should be set to false first if we don't want workers to log their deployment
python manage.py shell < "init.py"
python manage.py shell < "log.py"

# Instantiate the database if set to true
if [ "$CREATE_SAMPLE_DATA" = "true" ]; then
  echo "Creating sample data..."
  python manage.py create_sample_data
fi
