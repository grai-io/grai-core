# chat/consumers.py
import json

from django.core.cache import cache
from channels.generic.websocket import AsyncConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from users.models import User
from grAI.openai import get_chat_conversation, BaseConversation
from functools import cached_property, partial
from typing import Callable


class ChatConsumer(WebsocketConsumer):
    """
    scope includes: path, headers, method, user, and url_route
    """

    # cacheing has not been fully tested and should not be enabled without further evaluation.
    cacheing = False

    @cached_property
    def conversation(self) -> BaseConversation:
        conversation = get_chat_conversation()
        return conversation

    @cached_property
    def send_function(self) -> Callable:
        sending_function = async_to_sync(self.channel_layer.group_send)
        return partial(sending_function, self.group_name)

    @property
    def user(self) -> User:
        return self.scope["user"]

    @property
    def workspace(self) -> str:
        return self.scope["metadata"]["workspace_id"]

    @property
    def group_name(self) -> str:
        return f"{self.user.id}_{self.workspace}"

    @property
    def cache_id(self) -> str:
        return f"grAI:user:{self.user.id}:workspace:{self.workspace}"

    def update_cache(self, message):
        if self.cacheing:
            messages = cache.get_or_set(self.cache_id, [])
            messages.append(message)
            cache.aset(self.cache_id, messages)

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        if self.cacheing:
            cache.delete(self.cache_id)
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        ##self.send_function({"type": "chat.message", "message": message})
        response = self.conversation.request(message)
        self.send_function({"type": "chat.message", "message": response})
        self.update_cache(response)

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        self.update_cache(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
