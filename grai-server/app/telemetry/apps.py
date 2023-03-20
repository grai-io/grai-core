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
