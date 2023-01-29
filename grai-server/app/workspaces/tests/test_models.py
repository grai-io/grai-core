import datetime
import uuid

import pytest
from django_multitenant.utils import set_current_tenant

from workspaces.models import Organisation, Workspace


@pytest.mark.django_db
def test_organisation_created():
    organisation = Organisation.objects.create(name="O1")

    assert organisation.id == uuid.UUID(str(organisation.id))
    assert organisation.name == "O1"
    assert str(organisation) == "O1"
    assert isinstance(organisation.created_at, datetime.datetime)
    assert isinstance(organisation.updated_at, datetime.datetime)


@pytest.mark.django_db
def test_workspace_created():
    organisation = Organisation.objects.create(name="O1")
    workspace = Workspace.objects.create(name="abc", organisation=organisation)

    assert workspace.id == uuid.UUID(str(workspace.id))
    assert workspace.name == "abc"
    assert str(workspace) == "abc"
    assert workspace.ref() == "O1/abc"
    assert isinstance(workspace.created_at, datetime.datetime)
    assert isinstance(workspace.updated_at, datetime.datetime)


@pytest.mark.django_db
def test_workspace_created_from_load():
    set_current_tenant(None)
    organisation = Organisation.objects.create(name="O1")
    workspace = Workspace.objects.create(name="abc", organisation=organisation)
    workspaces = list(Workspace.objects.filter(name="abc").all())
    assert len(workspaces) == 1
    workspace2 = workspaces[0]
    attrs = ["id", "name"]
    for attr in attrs:
        assert getattr(workspace, attr) == getattr(workspace2, attr)
