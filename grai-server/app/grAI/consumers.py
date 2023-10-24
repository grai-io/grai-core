# chat/consumers.py
import json
import uuid

from django.core.cache import cache
from channels.generic.websocket import AsyncConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from users.models import User
from grAI.chat_implementations import get_chat_conversation, BaseConversation
from functools import cached_property, partial
from typing import Callable
from grAI.models import UserChat, Message
from workspaces.models import Membership
from django.conf import settings


class ChatConsumer(WebsocketConsumer):
    """
    scope includes: path, headers, method, user, and url_route
    """

    def __init__(self, *args, **kwargs):
        self._user_chat = None
        self.conversations: dict[uuid.UUID, BaseConversation] = {}
        super().__init__(*args, **kwargs)

    @property
    def user_chat(self) -> UserChat:
        if self._user_chat is None:
            self.user_chat = uuid.uuid4()

        return self._user_chat

    @user_chat.setter
    def user_chat(self, value: UserChat | uuid.UUID):
        if isinstance(value, UserChat):
            chat_obj = value
        elif isinstance(self._user_chat, UserChat) and value == self._user_chat.id:
            return
        else:
            try:
                chat_obj = UserChat.objects.filter(pk=value).get()
            except:
                chat_obj = UserChat(membership=self.membership)
                chat_obj.save()

        if chat_obj.membership != self.membership:
            raise ValueError(f"User does not have permission to view chat session `{chat_obj.id}` ")

        self._user_chat = chat_obj

    @cached_property
    def send_function(self) -> Callable:
        return partial(async_to_sync(self.channel_layer.group_send), self.group_name)

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
    def group_name(self) -> str:
        return f"{self.user.id}_{self.workspace}"

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def save(self, message: str, role: str, visible: bool):
        new_message = Message(chat=self.user_chat, message=message, role=role, visible=visible)
        new_message.save()

    # Receive message from WebSocket
    def receive(self, text_data: str | None = None, bytes_data: bytes | None = None):
        if text_data is None:
            raise ValueError("Text data must be provided to this websocket")

        text_data = json.loads(text_data)
        message = text_data["message"]
        self.user_chat = uuid.UUID(text_data["chat_id"]) if text_data["chat_id"] != "" else uuid.uuid4()

        self.save(message=message, role="user", visible=True)

        if not settings.HAS_OPENAI:
            response = (
                "OpenAI is currently disabled. In order to use AI components please enable ChatGPT on this instance of "
                "Grai"
            )
            agent = "system"
        elif not self.membership.workspace.ai_enabled:
            response = (
                "AI enabled chat has been disabled for your workspace. Please contact an administrator if you wish to "
                "enable these features."
            )
            agent = "system"
        else:
            if self.user_chat.id not in self.conversations:
                self.conversations[self.user_chat.id] = get_chat_conversation(self.user_chat.id)

            response = self.conversations[self.user_chat.id].request(message)
            agent = "assistant"

        self.send_function({"type": "chat.message", "message": response, "chat_id": str(self.user_chat.id)})
        self.save(message=response, role=agent, visible=True)

    # Receive message from room group
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
