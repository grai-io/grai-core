import os
import time
import posthog
from django.conf import settings

time.sleep(5)
posthog.disabled = settings.DISABLE_TELEMETRY
posthog.project_api_key = settings.POSTHOG_PROJECT_API_KEY
posthog.host = settings.POSTHOG_HOST
# if not settings.DISABLE_POSTHOG:
# if settings.ALLOWED_TO_LOG_POSTHOG and not settings.DISABLE_TELEMETRY:
#     posthog.capture(
#         settings.USER_ID,
#         event="Server Deployment",
#         groups={"package": "id:grai-server", "name": "grai-server", "version": settings.SERVER_VERSION},
#     )

print(settings.CELERY_IS_CELERY)
print(f"STARTUP LOGS WERE {os.environ.get('DISABLE_STARTUP_LOGS', 'False')}")
# log_deployment()
