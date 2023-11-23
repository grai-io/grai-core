# chat/consumers.py
import json
import logging
import uuid
from functools import cached_property, partial
from typing import Callable, ParamSpec, TypeVar
from uuid import UUID

from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.cache import cache
from pydantic import ValidationError
from functools import wraps
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from grAI.chat_implementations import BaseConversation, get_chat_conversation
from grAI.models import Message, MessageRoles, UserChat
from grAI.websocket_payloads import ChatErrorMessages, ChatEvent
from users.models import User
from workspaces.models import Membership
from asyncio import gather
from grai_schemas.serializers import dump_json

P = ParamSpec("P")
R = TypeVar("R")


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
                try:
                    # validate the payload
                    event = ChatEvent(**data)
                except ValidationError as e:
                    payload = {"error": f"Invalid payload:\n{e}"}
                    await self.send(text_data=json.dumps(payload))
                    return

                broadcast_payload = {**data, "type": "group.broadcast", "channel_name": self.channel_name}
                await self.channel_layer.group_send(self.group_name, broadcast_payload)
                await self.chat_message(event)
            case None:
                raise ValueError("Message type not specified")
            case _:
                await self.channel_layer.group_send(self.group_name, data)

    async def group_broadcast(self, payload: dict):
        # Handles not sending the message back to the original sender
        if payload["channel_name"] == self.channel_name:
            return

        await self.send(text_data=json.dumps(payload))

    async def chat_message(self, event: ChatEvent):
        # Insure the conversation exists
        if event.chat_id not in self.active_chats:
            chat, created = await async_get_or_create(UserChat, membership=self.membership, id=event.chat_id)
            self.active_chats.add(chat.id)

        if not settings.HAS_OPENAI:
            response = ChatErrorMessages.MISSING_OPENAI.value
            agent = MessageRoles.SYSTEM.value
        elif not self.membership.workspace.ai_enabled:
            response = ChatErrorMessages.WORKSPACE_AI_NOT_ENABLED.value
            agent = MessageRoles.SYSTEM.value
        else:
            if event.chat_id not in self.conversations:
                conversation = await get_chat_conversation(event.chat_id, workspace=self.workspace)
                self.conversations[event.chat_id] = conversation

            response = await self.conversations[event.chat_id].request(event.message)
            agent = MessageRoles.AGENT.value

        inbound_message = Message(
            chat_id=event.chat_id, message=event.message, role=MessageRoles.USER.value, visible=True
        )
        response_message = Message(chat_id=event.chat_id, message=response, role=agent, visible=True)

        response = {"message": response, "chat_id": str(event.chat_id)}
        broadcast_response = {**response, "type": "group.broadcast", "channel_name": self.channel_name}

        await gather(
            async_bulk_create_objects(Message, [inbound_message, response_message]),
            self.send(text_data=json.dumps(response)),
            self.channel_layer.group_send(self.group_name, broadcast_response),
        )
