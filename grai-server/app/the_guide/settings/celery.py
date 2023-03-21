from ..settings.prod import *
import os

DISABLE_POSTHOG = config("DISABLE_POSTHOG", default=True, cast=cast_string_to_bool(True))
