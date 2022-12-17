import hashlib

from decouple import config

from ..settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = config("SECRET_KEY")  # Default secret_key generated in entrypoint.sh
USER_ID = hashlib.md5(SECRET_KEY.encode()).hexdigest()
