"""
ASGI config for the_guide project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from typing import Any, Dict, Optional

import django
from django.core.asgi import get_asgi_application
from django.urls import re_path
from strawberry.channels import GraphQLHTTPConsumer as BaseGraphQLHTTPConsumer

django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_guide.settings.prod")
django_asgi_app = get_asgi_application()

from dataclasses import dataclass

from django.contrib.auth.models import AnonymousUser
from overrides import override
from strawberry.channels import ChannelsConsumer, ChannelsRequest
from strawberry.http.temporal_response import TemporalResponse

from api.schema import schema
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

# from asgi_cors_strawberry import CorsMiddleware
from grAI.authentication import WorkspacePathAuthMiddleware
from grAI.routing import websocket_urlpatterns


@dataclass
class ChannelsContext:
    request: ChannelsRequest
    response: TemporalResponse

    @property
    def user(self):
        # Depends on Channels' AuthMiddlewareStack
        if "user" in self.request.consumer.scope:
            return self.request.consumer.scope["user"]

        return AnonymousUser()

    @property
    def session(self):
        # Depends on Channels' SessionMiddleware / AuthMiddlewareStack
        if "session" in self.request.consumer.scope:
            return self.request.consumer.scope["session"]

        return None


@dataclass
class ChannelsWSContext:
    request: ChannelsConsumer
    connection_params: Optional[Dict[str, Any]] = None

    @property
    def ws(self) -> ChannelsConsumer:
        return self.request


class GraphQLHTTPConsumer(BaseGraphQLHTTPConsumer):
    @override
    async def get_context(self, request: ChannelsRequest, response: TemporalResponse) -> ChannelsContext:
        return ChannelsContext(
            request=request,
            response=response,
        )


gql_http_consumer = AuthMiddlewareStack(GraphQLHTTPConsumer.as_asgi(schema=schema))

app = ProtocolTypeRouter(
    {
        "http": URLRouter(
            [
                re_path("^graphql", gql_http_consumer),
                re_path("^", django_asgi_app),  # This might be another endpoint in your app
            ]
        ),
        "websocket": SessionMiddlewareStack(
            AuthMiddlewareStack(WorkspacePathAuthMiddleware(URLRouter(websocket_urlpatterns)))
        ),
    }
)

import fnmatch

ACCESS_CONTROL_ALLOW_ORIGIN = b"Access-Control-Allow-Origin"
ACCESS_CONTROL_ALLOW_HEADERS = b"Access-Control-Allow-Headers"
ACCESS_CONTROL_ALLOW_CREDENTIALS = b"Access-Control-Allow-Credentials"
CONTENT_TYPE = b"content-type"
DEFAULT_HEADERS = {
    ACCESS_CONTROL_ALLOW_ORIGIN,
    ACCESS_CONTROL_ALLOW_HEADERS,
    CONTENT_TYPE,
}


def cors_options(allow_all=True, hosts=[], host_wildcards=[], headers=["content-type"]):
    hosts = set(h.encode("utf8") if isinstance(h, str) else h for h in hosts)
    host_wildcards = [h.encode("utf8") if isinstance(h, str) else h for h in host_wildcards]
    headers = [h.encode("utf8") if isinstance(h, str) else h for h in headers]

    return allow_all, hosts, host_wildcards, headers


class CorsMiddleware:
    def __init__(self, app, allow_all=True, hosts=[], host_wildcards=[], headers=["content-type"]):
        self.app = app
        (
            self.allow_all,
            self.hosts,
            self.host_wildcards,
            self.access_control_allow_headers,
        ) = cors_options(allow_all, hosts, host_wildcards, headers)

    async def __call__(self, scope, receive, send):
        async def _base_send(event):
            if event["type"] == "http.response.start":
                original_headers = event.get("headers") or []  # send_headers
                access_control_allow_origin = None
                if self.allow_all:
                    access_control_allow_origin = b"*"
                elif self.hosts or self.host_wildcards:
                    incoming_origin = dict(scope.get("headers") or []).get(b"origin")
                    if incoming_origin:
                        matches_hosts = incoming_origin in self.hosts
                        matches_wildcards = any(
                            fnmatch.fnmatch(incoming_origin, host_wildcard) for host_wildcard in self.host_wildcards
                        )
                        if matches_hosts or matches_wildcards:
                            access_control_allow_origin = incoming_origin

                if access_control_allow_origin:
                    # preflight in consumer -> status is 405
                    status = 200 if scope["method"] == "OPTIONS" else event["status"]
                    event = {
                        "type": "http.response.start",
                        "status": status,
                        "headers": [h for h in original_headers if h[0] not in DEFAULT_HEADERS]
                        + [
                            (ACCESS_CONTROL_ALLOW_ORIGIN, access_control_allow_origin),
                            (
                                ACCESS_CONTROL_ALLOW_HEADERS,
                                b", ".join(self.access_control_allow_headers),
                            ),
                            (ACCESS_CONTROL_ALLOW_CREDENTIALS, b"true"),
                        ],
                    }
            await send(event)

        # _base_send -> send in ASGIHandler or AsyncConsumer
        return await self.app(scope, receive, _base_send)


application = CorsMiddleware(
    app,
    allow_all=False,
    hosts=["http://localhost:3000", "http://localhost:8000"],
    host_wildcards=[],
    headers=["content-type"],
)
