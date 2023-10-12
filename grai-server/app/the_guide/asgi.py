"""
ASGI config for the_guide project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

django.setup()
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from grAI.authentication import WorkspacePathAuthMiddleware
from grAI.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_guide.settings.prod")
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": SessionMiddlewareStack(
            AuthMiddlewareStack(WorkspacePathAuthMiddleware(URLRouter(websocket_urlpatterns)))
        ),
    }
)
