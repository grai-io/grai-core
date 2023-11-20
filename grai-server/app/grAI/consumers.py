# chat/consumers.py
import json
import logging
import uuid
from functools import cached_property, partial
from typing import Callable
from uuid import UUID

from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.cache import cache
from pydantic import ValidationError

from channels.generic.websocket import AsyncConsumer, WebsocketConsumer
from grAI.chat_implementations import BaseConversation, get_chat_conversation
from grAI.models import Message, MessageRoles, UserChat
from grAI.websocket_payloads import ChatErrorMessages, ChatEvent
from users.models import User
from workspaces.models import Membership


class ChatConsumer(WebsocketConsumer):
    """
    scope includes: path, headers, method, user, and url_route
    """

    def __init__(self, *args, **kwargs):
        self.conversations: dict[UUID, BaseConversation] = {}
        self.active_chats: set[UUID] = set()
        super().__init__(*args, **kwargs)

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

    def receive(self, text_data):
        data: dict = json.loads(text_data)
        socket_message_type = data.get("type", None)
        match socket_message_type:
            case "chat.message":
                self.chat_message(data)
            case None:
                raise ValueError("Message type not specified")
            case _:
                raise ValueError(f"Unknown message type `{socket_message_type}`")

    def chat_message(self, event: dict):
        try:
            payload = ChatEvent(**event)
        except ValidationError as e:
            response = f"Invalid payload:\n{e}"
            self.send(text_data=json.dumps({"error": response}))
            return

        # Insure the conversation exists
        if payload.chat_id not in self.active_chats:
            chat, created = UserChat.objects.get_or_create(membership=self.membership, id=payload.chat_id)
            self.active_chats.add(chat.id)

        if not settings.HAS_OPENAI:
            response = ChatErrorMessages.MISSING_OPENAI.value
            agent = MessageRoles.SYSTEM.value
        elif not self.membership.workspace.ai_enabled:
            response = ChatErrorMessages.WORKSPACE_AI_NOT_ENABLED.value
            agent = MessageRoles.SYSTEM.value
        else:
            if payload.chat_id not in self.conversations:
                self.conversations[payload.chat_id] = get_chat_conversation(payload.chat_id, workspace=self.workspace)

            response = self.conversations[payload.chat_id].request(payload.message)
            agent = MessageRoles.AGENT.value

        response_payload = ChatEvent(message=response, chat_id=payload.chat_id)

        inbound_message = Message(
            chat_id=payload.chat_id, message=payload.message, role=MessageRoles.USER.value, visible=True
        )
        response_message = Message(chat_id=payload.chat_id, message=response, role=agent, visible=True)
        Message.objects.bulk_create([inbound_message, response_message])

        self.send(text_data=response_payload.json())
