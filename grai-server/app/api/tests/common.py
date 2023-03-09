import uuid
from importlib import import_module

import pytest
import pytest_asyncio
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest

from connections.models import Connection, Connector
from workspaces.models import Membership, Organisation, Workspace


class Context(object):
    pass


@pytest.fixture
async def test_organisation():
    organisation, created = await Organisation.objects.aget_or_create(name="Test Organisation")

    return organisation


@pytest_asyncio.fixture
async def test_user():
    User = get_user_model()

    user = User()
    user.set_password("password")
    await sync_to_async(user.save)()

    return user


@pytest_asyncio.fixture
async def test_workspace(test_organisation):
    workspace = await Workspace.objects.acreate(name=str(uuid.uuid4()), organisation=test_organisation)

    return workspace


@pytest_asyncio.fixture
async def test_context(test_organisation, test_workspace, test_user):
    membership = await Membership.objects.acreate(user=test_user, workspace=test_workspace, role="admin")

    request = HttpRequest
    request.user = test_user

    context = Context()
    context.request = request

    engine = import_module(settings.SESSION_ENGINE)
    session_key = None
    context.request.session = engine.SessionStore(session_key)
    context.request.META = {}

    return context, test_organisation, test_workspace, test_user, membership


@pytest_asyncio.fixture
async def test_basic_context():
    request = HttpRequest
    request.user = None

    context = Context()
    context.request = request

    engine = import_module(settings.SESSION_ENGINE)
    session_key = None
    context.request.session = engine.SessionStore(session_key)
    context.request.META = {}

    return context


def generate_username():
    return f"{str(uuid.uuid4())}@gmail.com"


def generate_workspace_name():
    return f"Workspace {str(uuid.uuid4())}"


def generate_connector_name():
    return f"Connector {str(uuid.uuid4())}"


def generate_connection_name():
    return f"Connection {str(uuid.uuid4())}"


async def generate_workspace(organisation: Organisation):
    return await Workspace.objects.acreate(name=generate_workspace_name(), organisation=organisation)


async def generate_connector():
    return await Connector.objects.acreate(name=generate_connector_name())


async def generate_connection(workspace: Workspace, connector: Connector = None, temp: bool = False):
    connector = connector if connector else await generate_connector()

    return await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name=generate_connection_name(),
        metadata={},
        secrets={},
        temp=temp,
    )
