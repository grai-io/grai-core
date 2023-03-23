import os
import time

import posthog
from django.conf import settings

posthog.disabled = settings.DISABLE_TELEMETRY
posthog.project_api_key = settings.POSTHOG_PROJECT_API_KEY
posthog.host = settings.POSTHOG_HOST

if not settings.DISABLE_POSTHOG and not settings.DISABLE_TELEMETRY:
    posthog.capture(
        settings.USER_ID,
        event="Server Deployment",
        groups={"package": "id:grai-server", "name": "grai-server", "version": settings.SERVER_VERSION},
    )
