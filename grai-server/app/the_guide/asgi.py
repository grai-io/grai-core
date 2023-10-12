"""
ASGI config for the_guide project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

# from grAI.urls import router as grAI_router


from grAI.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_guide.settings.prod")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": SessionMiddlewareStack(AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
    }
)
