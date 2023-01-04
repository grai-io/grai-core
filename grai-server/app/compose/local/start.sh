#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

gunicorn the_guide.wsgi -b 0.0.0.0:8000 -w 2