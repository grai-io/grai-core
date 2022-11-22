import os
import uuid

import posthog
import sentry_sdk
from django.apps import AppConfig
from django.conf import settings
from posthog.sentry.posthog_integration import PostHogIntegration
from sentry_sdk import configure_scope
from sentry_sdk.integrations.django import DjangoIntegration

disable_telemetry = os.environ.get("DISABLE_TELEMETRY", False)
server_version = os.environ.get("GRAI_SERVER_VERSION", "unknown")

try:
    # https://posthog.com/docs/integrate/server/python

    if not disable_telemetry:
        sentry_sdk.init(
            dsn="https://3ef0d6800e084eae8b3a8f4ee4be1d3d@o4503978528407552.ingest.sentry.io/4503978529456128",
            traces_sample_rate=1.0,
            integrations=[DjangoIntegration(), PostHogIntegration()],
            release=f"grai-server@{server_version}",
        )

        with configure_scope() as scope:
            scope.set_tag("posthog_org_id", settings.USER_ID)
except:
    # Don't break anything for the user if something happens with the telemetry
    pass


class TelemetryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telemetry"

    def ready(self):
        posthog.disabled = disable_telemetry
        PostHogIntegration.organization = settings.USER_ID
        posthog.project_api_key = "phc_Q8OCDm0JpCwt4Akk3pMybuBWniWPfOsJzRrdxWjAnjE"
        posthog.host = "https://app.posthog.com"

        group_properties = {
            "name": "grai-server",
        }
        if os.environ.get("BEGIN_LOGGING", False):
            posthog.capture(
                settings.USER_ID,
                event="Server Deployment",
                groups={"package": "id:grai-server", "name": "grai-server"},
                # properties={"$group_set": group_properties}
            )
            # posthog.group_identify('package', 'id:grai-server', {
            #     'name': 'grai-server',
            # })
