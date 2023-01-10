#!/bin/bash

set -o errexit
set -o nounset

celery -A the_guide worker -l INFO
