import json

import pytest
from grai_schemas.human_ids import get_human_id

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from users.models import User
from workspaces.models import (  # Import your Membership model
    Membership,
    Organisation,
    Workspace,
)


@pytest.fixture
def user() -> User:
    return User.objects.create(username=f"{get_human_id()}@grai.io")


@pytest.fixture
def organisation() -> Organisation:
    return Organisation.objects.create(name=get_human_id())  #


@pytest.fixture
def workspace(organisation) -> Workspace:
    return Workspace.objects.create(name=get_human_id(), organisation=organisation)


@pytest.fixture
async def membership(user, workspace) -> Membership:
    return await database_sync_to_async(Membership.objects.create)(user=user, workspace=workspace, is_active=True)


class SimpleApplication(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": message}))


@pytest.fixture
def simple_application():
    return SimpleApplication()


@pytest.fixture
def middleware(simple_application):
    from grAI.authentication import WorkspacePathAuthMiddleware

    return WorkspacePathAuthMiddleware(simple_application)
