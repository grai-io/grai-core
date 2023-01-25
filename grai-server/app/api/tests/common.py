from importlib import import_module

import pytest
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http.request import HttpRequest

from workspaces.models import Membership, Workspace


class Context(object):
    pass


@pytest.fixture
async def test_context():
    User = get_user_model()

    workspace = await Workspace.objects.acreate(name="Test Workspace")
    user = User()
    user.set_password("password")
    await sync_to_async(user.save)()

    await Membership.objects.acreate(user=user, workspace=workspace, role="admin")

    request = HttpRequest
    request.user = user

    context = Context()
    context.request = request

    engine = import_module(settings.SESSION_ENGINE)
    session_key = None
    context.request.session = engine.SessionStore(session_key)
    context.request.META = {}

    return context, workspace, user


@pytest.fixture
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
