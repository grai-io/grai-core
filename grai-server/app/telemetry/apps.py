import os
import uuid

import posthog
import sentry_sdk
from django.apps import AppConfig
from django.conf import settings
from posthog.sentry.posthog_integration import PostHogIntegration
from sentry_sdk import configure_scope
from sentry_sdk.integrations.django import DjangoIntegration

PostHogIntegration.organization = settings.USER_ID

if not settings.DISABLE_TELEMETRY:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
        integrations=[DjangoIntegration(), PostHogIntegration()],
        release=f"grai-server@{settings.SERVER_VERSION}",
    )
    with configure_scope() as scope:
        scope.set_tag("posthog_org_id", settings.USER_ID)


# class TelemetryConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "telemetry"
#
#     def ready(self):
#         posthog.disabled = settings.DISABLE_TELEMETRY
#
#         posthog.project_api_key = settings.POSTHOG_PROJECT_API_KEY
#         posthog.host = settings.POSTHOG_HOST
#
#         group_properties = {
#             "name": "grai-server",
#         }
#         if not settings.DISABLE_TELEMETRY and os.environ.get("BEGIN_LOGGING") == "True":
#             print("OOPSIES, HOW MANY TIMES WE WILL BE HERE: ", os.environ.get("BEGIN_LOGGING", "a_default"))
#             posthog.capture(
#                 settings.USER_ID,
#                 event="Server Deployment",
#                 groups={"package": "id:grai-server", "name": "grai-server", "version": settings.SERVER_VERSION},
#             )
