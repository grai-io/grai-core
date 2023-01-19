import json
import uuid
from itertools import product

import django.db.utils
import pytest
from django.urls import reverse

from lineage.urls import app_name
from workspaces.models import Membership, Organisation, Workspace, WorkspaceAPIKey


@pytest.fixture
def create_organisation(name=None):
    return Organisation.objects.create(name=uuid.uuid4() if name is None else name)


@pytest.fixture
def create_workspace(create_organisation, name=None):
    return Workspace.objects.create(
        name=uuid.uuid4() if name is None else name, organisation=create_organisation
    )


@pytest.fixture
def test_password():
    return "strong-test-pass"


def generate_username():
    return f"{str(uuid.uuid4())}@gmail.com"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        kwargs.setdefault("username", generate_username())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(client, create_user, test_password, create_workspace):
    def make_auto_login(user=None, workspace=None):
        if user is None:
            user = create_user()
            client.login(username=user.username, password=test_password)
        if workspace is None:
            workspace = create_workspace
        Membership.objects.create(role="admin", user=user, workspace=workspace)
        return client, user, workspace

    return make_auto_login


@pytest.mark.django_db
def test_get_workspaces(auto_login_user):
    client, user, workspace = auto_login_user()
    url = reverse("workspaces:workspaces-list")
    response = client.get(url)
    assert (
        response.status_code == 200
    ), f"verb `get` failed on workspaces with status {response.status_code}"
    workspaces = list(response.json())
    assert len(workspaces) == 1


@pytest.mark.django_db
def test_get_workspaces_no_membership(auto_login_user, create_organisation):
    client, user, workspace = auto_login_user()
    Workspace.objects.create(name="abc2", organisation=create_organisation)
    url = reverse("workspaces:workspaces-list")
    response = client.get(url)
    assert (
        response.status_code == 200
    ), f"verb `get` failed on workspaces with status {response.status_code}"
    workspaces = list(response.json())
    assert len(workspaces) == 1


@pytest.mark.django_db
def test_get_workspace(auto_login_user):
    client, user, workspace = auto_login_user()
    url = reverse("workspaces:workspaces-detail", kwargs={"pk": str(workspace.id)})
    response = client.get(url)
    assert (
        response.status_code == 200
    ), f"verb `get` failed on workspaces with status {response.status_code}"


@pytest.mark.django_db
def test_get_workspace_no_membership(auto_login_user, create_organisation):
    client, user, workspace = auto_login_user()
    workspace2 = Workspace.objects.create(name="abc2", organisation=create_organisation)
    url = reverse("workspaces:workspaces-detail", kwargs={"pk": str(workspace2.id)})
    response = client.get(url)
    assert (
        response.status_code == 404
    ), f"verb `get` failed on workspaces with status {response.status_code}"
