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
from grAI.models import UserChat, Message
from workspaces.models import Membership
from django.conf import settings


class ChatConsumer(WebsocketConsumer):
    """
    scope includes: path, headers, method, user, and url_route
    """

    def __init__(self, *args, **kwargs):
        self._user_chat = None
        self._conversation = None
        super().__init__(*args, **kwargs)

    @property
    def user_chat(self) -> UserChat:
        if self._user_chat is None:
            self._user_chat = UserChat(membership=self.membership)
            self._user_chat.save()

        return self._user_chat

    @user_chat.setter
    def user_chat(self, value: UserChat | uuid.UUID):
        chat_id = value if isinstance(value, uuid.UUID) else value.id

        if self._user_chat is None:
            chat_obj = value if isinstance(value, UserChat) else UserChat.objects.filter(pk=value)

            if chat_obj.membership != self.membership:
                raise ValueError(f"User does not have permission to view chat session `{value}` ")

            self._user_chat = chat_obj
        elif chat_id != self._user_chat.id:
            raise ValueError(f"Provided chat id {chat_id} does not match the current chat.")

    def chat_cache_id(self, chat_id):
        return f"grAI:chat_id:{chat_id}"

    @property
    def conversation(self) -> BaseConversation:
        if self._conversation is None:
            self._conversation = get_chat_conversation()

        return self._conversation

    @conversation.setter
    def conversation(self, value: BaseConversation):
        self._conversation = value

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
    def group_name(self) -> str:
        return f"{self.user.id}_{self.workspace}"

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def save(self, message: str, role: str, visible: bool):
        new_message = Message(chat=self.chat.id, message=message, role=role, visible=visible)
        new_message.save()

    # Receive message from WebSocket
    def receive(self, text_data_string: str):
        text_data = json.loads(text_data_string)
        message = text_data["message"]
        chat_id = text_data["chat_id"]

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
            response = self.conversation.request(message, chat_id)
            agent = "agent"
        self.send_function({"type": "chat.message", "message": response})
        self.save(response, agent, True)

    # Receive message from room group
    def chat_message(self, event):
        self.send(text_data=json.dumps({k: event[k] for k in ["message", "chat_id"]}))
        self.save(event["message"], "user", True)
