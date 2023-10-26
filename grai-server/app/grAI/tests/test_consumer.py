import json
import uuid

import pytest
from django.test import override_settings

from channels.testing import WebsocketCommunicator
from grAI.authentication import WorkspacePathAuthMiddleware
from grAI.consumers import ChatConsumer
from grAI.websocket_payloads import ChatErrorMessages


@pytest.fixture
def chat_consumer_app():
    return WorkspacePathAuthMiddleware(ChatConsumer.as_asgi())


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestChatConsumer:
    async def test_save_openai_disabled(self, chat_consumer_app, membership):
        communicator = WebsocketCommunicator(chat_consumer_app, f"ws:/chat/{membership.workspace.id}/")
        communicator.scope["user"] = membership.user
        connected, subprotocol = await communicator.connect()
        assert connected

        with override_settings(OPENAI_ENABLED=False):
            await communicator.send_json_to(
                {"type": "chat.message", "message": "some text", "chat_id": f"{uuid.uuid4()}"}
            )

            response = await communicator.receive_json_from()
            assert response["message"] == ChatErrorMessages.MISSING_OPENAI.value

        await communicator.disconnect()

    async def test_save_workspace_not_ai_enabled(self, chat_consumer_app, membership, workspace):
        workspace.ai_enabled = False
        await workspace.asave()

        communicator = WebsocketCommunicator(chat_consumer_app, f"ws:/chat/{membership.workspace.id}/")
        communicator.scope["user"] = membership.user
        connected, subprotocol = await communicator.connect()
        assert connected

        with override_settings(HAS_OPENAI=True):
            await communicator.send_json_to(
                {"type": "chat.message", "message": "some text", "chat_id": f"{uuid.uuid4()}"}
            )

            response = await communicator.receive_json_from()
            assert response["message"] == ChatErrorMessages.WORKSPACE_AI_NOT_ENABLED.value

        await communicator.disconnect()

    # Invalid payload test
    async def test_invalid_payload(self, chat_consumer_app, membership):
        communicator = WebsocketCommunicator(chat_consumer_app, f"ws:/chat/{membership.workspace.id}/")
        communicator.scope["user"] = membership.user
        connected, subprotocol = await communicator.connect()
        assert connected

        await communicator.send_json_to(
            {"type": "chat.message", "an_invalid_key": "some text", "chat_id": f"{uuid.uuid4()}"}
        )

        response = await communicator.receive_json_from()
        assert "error" in response

        await communicator.disconnect()
