#!/bin/bash

set -o errexit
set -o nounset

celery -A the_guide beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler