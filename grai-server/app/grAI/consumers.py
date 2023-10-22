# chat/consumers.py
import json
import uuid

from django.core.cache import cache
from channels.generic.websocket import AsyncConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from users.models import User
from grAI.openai import get_chat_conversation, BaseConversation
from functools import cached_property, partial
from typing import Callable
from grAI.models import UserChat
from workspaces.models import Membership


class UserChatHandler:
    def __init__(self, membership: Membership, chat_id: uuid.UUID | None = None, message_number: int | None = None):
        self.membership = membership
        self.chat_id = chat_id if chat_id is not None else uuid.uuid4()
        self.current_message = message_number

    def save(self, message: str, role: str):
        if self.current_message is None:
            chat = UserChat(membership=self.membership, chat_id=self.chat_id, message=message, role=role)
        else:
            chat = UserChat(
                membership=self.membership,
                chat_id=self.chat_id,
                message=message,
                role=role,
                message_number=self.current_message + 1,
            )
        chat.save()
        self.current_message = chat.message_number


class ChatConsumer(WebsocketConsumer):
    """
    scope includes: path, headers, method, user, and url_route
    """

    # cacheing has not been fully tested and should not be enabled without further evaluation.
    cacheing = False

    @cached_property
    def user_chat(self):
        return UserChatHandler(membership=self.membership, chat_id=self.chat_id)

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
    def membership(self) -> Membership:
        return self.scope["metadata"]["membership"]

    @property
    def chat_id(self):
        return self.scope["metadata"].get("chat_id", uuid.uuid4())

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

    def save(self, message: str, role: str):
        self.update_cache(message)
        self.user_chat.save(message, role)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if not self.membership.workspace.ai_enabled:
            response = (
                "AI enabled chat has been disabled for your workspace. Please contact an administrator if you wish to "
                "enable these features."
            )
            agent = "system"
        else:
            response = self.conversation.request(message)
            agent = "agent"

        self.send_function({"type": "chat.message", "message": response})
        self.save(response, agent)

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
        self.save(message, "user")
