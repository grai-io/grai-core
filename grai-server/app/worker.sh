#!/bin/bash

set -o errexit
set -o nounset

mkdir -p /var/run/celery /var/log/celery
chown -R nobody:nogroup /var/run/celery /var/log/celery

celery -A the_guide worker -l INFO --uid=nobody --gid=nogroup
