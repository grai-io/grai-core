import pytest
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from workspaces.models import Membership, Workspace


class Info(object):
    pass


@pytest.fixture
async def test_info():
    User = get_user_model()

    workspace = await Workspace.objects.acreate(name="Test Workspace")
    user = await User.objects.acreate()
    await Membership.objects.acreate(user=user, workspace=workspace, role="admin")

    request = HttpRequest
    request.user = user

    info = Info()
    info.request = request

    return info, workspace, user
