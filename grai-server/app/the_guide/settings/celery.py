import os

from ..settings.prod import *

DISABLE_POSTHOG = config("DISABLE_POSTHOG", default=True, cast=cast_string_to_bool(True))
