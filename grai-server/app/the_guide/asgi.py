"""
ASGI config for the_guide project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from django.urls import re_path
from django.core.asgi import get_asgi_application
from strawberry.channels import GraphQLHTTPConsumer, GraphQLWSConsumer

django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_guide.settings.prod")
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from asgi_cors_strawberry import CorsMiddleware
from grAI.authentication import WorkspacePathAuthMiddleware
from grAI.routing import websocket_urlpatterns
from api.schema import schema

gql_http_consumer = AuthMiddlewareStack(GraphQLHTTPConsumer.as_asgi(schema=schema))

application = ProtocolTypeRouter(
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

application = CorsMiddleware(application, allow_all=True)
