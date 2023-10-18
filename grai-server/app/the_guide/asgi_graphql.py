import fnmatch
from dataclasses import dataclass

from django.contrib.auth.models import AnonymousUser
from overrides import override
from strawberry.channels import ChannelsConsumer, ChannelsRequest
from strawberry.http.temporal_response import TemporalResponse
from strawberry.channels import GraphQLHTTPConsumer as BaseGraphQLHTTPConsumer
from typing import Any

ACCESS_CONTROL_ALLOW_ORIGIN = b"Access-Control-Allow-Origin"
ACCESS_CONTROL_ALLOW_HEADERS = b"Access-Control-Allow-Headers"
ACCESS_CONTROL_ALLOW_CREDENTIALS = b"Access-Control-Allow-Credentials"
CONTENT_TYPE = b"content-type"
DEFAULT_HEADERS = {
    ACCESS_CONTROL_ALLOW_ORIGIN,
    ACCESS_CONTROL_ALLOW_HEADERS,
    CONTENT_TYPE,
}


class A:
    pass


class B(A):
    extra = True


class SessionChannelsRequest(ChannelsRequest):
    def __init__(self, *args, META: dict | None = None, **kwargs):
        self.META = {} if META is None else META
        self._user = None
        super().__init__(*args, **kwargs)

    @classmethod
    def from_parent(cls, obj: ChannelsRequest):
        return cls(**vars(obj))

    @property
    def session(self):
        # Depends on Channels' SessionMiddleware / AuthMiddlewareStack
        if "session" in self.consumer.scope:
            return self.consumer.scope["session"]

        return None

    @property
    def user(self):
        if self._user is None:
            user = self.request.consumer.scope["user"] if "user" in self.request.consumer.scope else AnonymousUser()
            self.user = user

        return self._user

    @user.setter
    def user(self, value):
        self._user = value


@dataclass
class ChannelsContext:
    request: SessionChannelsRequest
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
    connection_params: dict[str, Any] | None = None

    @property
    def ws(self) -> ChannelsConsumer:
        return self.request


class GraphQLHTTPConsumer(BaseGraphQLHTTPConsumer):
    @override
    async def get_context(self, request: ChannelsRequest, response: TemporalResponse) -> ChannelsContext:
        ctx = ChannelsContext(
            request=SessionChannelsRequest.from_parent(request),
            response=response,
        )
        return ctx


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
