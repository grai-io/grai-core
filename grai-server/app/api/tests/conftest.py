import pytest
from conftest import test_membership

from grAI.models import Message, UserChat


@pytest.fixture
async def test_chat(test_membership):
    chat = await UserChat.objects.acreate(membership=test_membership)

    return chat


@pytest.fixture
async def test_message(test_chat):
    message = await Message.objects.acreate(chat=test_chat, message="Test message", role="user", visible=True)

    return message
