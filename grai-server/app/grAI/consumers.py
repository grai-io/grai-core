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

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from grAI.chat_implementations import BaseConversation, get_chat_conversation
from grAI.models import Message, MessageRoles, UserChat
from grAI.websocket_payloads import ChatErrorMessages, ChatEvent
from users.models import User
from workspaces.models import Membership


@database_sync_to_async
def async_bulk_create_objects(model, objects):
    model.objects.bulk_create(objects)


@database_sync_to_async
def async_get_or_create(model, **kwargs):
    return model.objects.get_or_create(**kwargs)


class ChatConsumer(AsyncWebsocketConsumer):
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

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data: dict = json.loads(text_data)

        match socket_message_type := data.get("type", None):
            case "chat.message":
                await self.chat_message(data)
            case None:
                raise ValueError("Message type not specified")
            case _:
                raise ValueError(f"Unknown message type `{socket_message_type}`")

    async def chat_message(self, event: dict):
        try:
            payload = ChatEvent(**event)
        except ValidationError as e:
            response = f"Invalid payload:\n{e}"
            await self.send(text_data=json.dumps({"error": response}))
            return

        # Insure the conversation exists
        if payload.chat_id not in self.active_chats:
            chat, created = await async_get_or_create(UserChat, membership=self.membership, id=payload.chat_id)
            self.active_chats.add(chat.id)

        if not settings.HAS_OPENAI:
            response = ChatErrorMessages.MISSING_OPENAI.value
            agent = MessageRoles.SYSTEM.value
        elif not self.membership.workspace.ai_enabled:
            response = ChatErrorMessages.WORKSPACE_AI_NOT_ENABLED.value
            agent = MessageRoles.SYSTEM.value
        else:
            if payload.chat_id not in self.conversations:
                conversation = await get_chat_conversation(payload.chat_id, workspace=self.workspace)
                self.conversations[payload.chat_id] = conversation

            response = await self.conversations[payload.chat_id].request(payload.message)
            agent = MessageRoles.AGENT.value

        response_payload = ChatEvent(message=response, chat_id=payload.chat_id)

        inbound_message = Message(
            chat_id=payload.chat_id, message=payload.message, role=MessageRoles.USER.value, visible=True
        )
        response_message = Message(chat_id=payload.chat_id, message=response, role=agent, visible=True)
        await async_bulk_create_objects(Message, [inbound_message, response_message])

        await self.send(text_data=response_payload.json())
