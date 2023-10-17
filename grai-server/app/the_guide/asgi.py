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


django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_guide.settings.prod")
django_asgi_app = get_asgi_application()


from api.schema import schema
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

# from asgi_cors_strawberry import CorsMiddleware
from grAI.authentication import WorkspacePathAuthMiddleware
from grAI.routing import websocket_urlpatterns
from django.conf import settings
from .asgi_graphql import GraphQLHTTPConsumer, CorsMiddleware


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


application = CorsMiddleware(
    app,
    allow_all=False,
    hosts=settings.ALLOWED_HOSTS,
    host_wildcards=[],
    headers=["content-type"],
)
