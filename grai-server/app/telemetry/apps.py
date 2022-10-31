import os
import uuid

import posthog
import sentry_sdk
from django.apps import AppConfig
from posthog.sentry.posthog_integration import PostHogIntegration
from sentry_sdk import configure_scope
from sentry_sdk.integrations.django import DjangoIntegration

orgname = uuid.uuid4()
PostHogIntegration.organization = orgname

try:
    # https://posthog.com/docs/integrate/server/python
    # TODO: Possibly come back to this later
    sentry_sdk.init(
        dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
        integrations=[DjangoIntegration(), PostHogIntegration()],
    )

    with configure_scope() as scope:
        scope.set_tag("posthog_distinct_id", "some distinct id")
except:
    # Don't break anything for the user if something happens with the telemetry
    pass


class TelemetryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telemetry"

    def ready(self):
        posthog.project_api_key = "phc_Q8OCDm0JpCwt4Akk3pMybuBWniWPfOsJzRrdxWjAnjE"
        posthog.host = "https://app.posthog.com"
        posthog.disabled = os.environ.get("DISABLE_TELEMETRY", False)

        posthog.capture(orgname, event="Server deployment", groups={"package": "grai-server"})
