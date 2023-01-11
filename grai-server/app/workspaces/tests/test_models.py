import datetime
import uuid

import pytest
from django_multitenant.utils import set_current_tenant

from workspaces.models import Workspace


@pytest.mark.django_db
def test_workspace_created():
    workspace = Workspace.objects.create(name="abc")

    assert workspace.id == uuid.UUID(str(workspace.id))
    assert workspace.name == "abc"
    assert isinstance(workspace.created_at, datetime.datetime)
    assert isinstance(workspace.updated_at, datetime.datetime)


@pytest.mark.django_db
def test_workspace_created_from_load():
    set_current_tenant(None)
    workspace = Workspace.objects.create(name="abc")
    workspaces = list(Workspace.objects.filter(name="abc").all())
    assert len(workspaces) == 1
    workspace2 = workspaces[0]
    attrs = ["id", "name"]
    for attr in attrs:
        assert getattr(workspace, attr) == getattr(workspace2, attr)
