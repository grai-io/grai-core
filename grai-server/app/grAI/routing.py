from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/chat/(?P<workspace>[a-zA-Z0-9-]+)/$", consumers.ChatConsumer.as_asgi()),
]
