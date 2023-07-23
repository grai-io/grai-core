#!/bin/bash

# Run database migrations
python manage.py migrate

# Seed database from json files
fixtures=$(ls seed/)
while IFS= read -r fixture; do
    echo -n "Seeding $fixture ..."
    echo $fixture
    python manage.py loaddata seed/$fixture
done <<< "$fixtures"

# Every call to manage.py imports telemetry/apps which have a log event but we only want the first.
# These should be set to false first if we don't want workers to log their deployment
python manage.py shell < "init.py"
python manage.py shell < "log.py"

# Instantiate the database if set to true
if [ "$CREATE_SAMPLE_DATA" = "true" ]; then
  echo "Creating sample data..."
  python manage.py create_sample_data
fi
