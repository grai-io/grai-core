import hashlib

from ..settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "This-Is-A-Test_key"
USER_ID = hashlib.md5(SECRET_KEY.encode()).hexdigest()

DISABLE_TELEMETRY = config("DISABLE_TELEMETRY", default=True, cast=cast_string_to_bool(True))

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
