import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http.request import HttpRequest
from asgiref.sync import sync_to_async
from django.conf import settings
from importlib import import_module
import pytest_asyncio

from workspaces.models import Membership, Organisation, Workspace


class Context(object):
    pass


@pytest_asyncio.fixture
async def test_organisation():
    return await Organisation.objects.acreate(name="Test Organisation")


@pytest_asyncio.fixture
async def test_user():
    User = get_user_model()

    user = User()
    user.set_password("password")
    await sync_to_async(user.save)()

    return user


@pytest_asyncio.fixture
async def test_context(test_organisation, test_user):
    workspace, created = await Workspace.objects.aget_or_create(
        name="Test Workspace", organisation=test_organisation
    )

    await Membership.objects.acreate(user=test_user, workspace=workspace, role="admin")

    request = HttpRequest
    request.user = test_user

    context = Context()
    context.request = request

    engine = import_module(settings.SESSION_ENGINE)
    session_key = None
    context.request.session = engine.SessionStore(session_key)
    context.request.META = {}

    return context, test_organisation, workspace, test_user


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
