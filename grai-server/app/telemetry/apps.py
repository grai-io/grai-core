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


def traces_sampler(ctx):
    if ctx["parent_sampled"] is not None:
        # If this transaction has a parent, we usually want to sample it
        # if and only if its parent was sampled.
        return ctx["parent_sampled"]
    op = ctx["transaction_context"]["op"]
    if "wsgi_environ" in ctx:
        # Get the URL for WSGI requests
        url = ctx["wsgi_environ"].get("PATH_INFO", "")
    elif "asgi_scope" in ctx:
        # Get the URL for ASGI requests
        url = ctx["asgi_scope"].get("path", "")
    else:
        # Other kinds of transactions don't have a URL
        url = ""
    if op == "http.server":
        # Conditions only relevant to operation "http.server"
        if url.startswith("/health/"):
            return 0  # Don't trace any of these transactions
    return settings.SENTRY_SAMPLE_RATE


if not settings.DISABLE_TELEMETRY:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sampler=traces_sampler,
        integrations=[DjangoIntegration(), PostHogIntegration()],
        release=f"grai-server@{settings.SERVER_VERSION}",
    )
    with configure_scope() as scope:
        scope.set_tag("posthog_org_id", settings.USER_ID)
