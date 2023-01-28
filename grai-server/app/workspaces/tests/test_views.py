import json
import uuid
from itertools import product

import django.db.utils
import pytest
from django.urls import reverse

from lineage.urls import app_name
from workspaces.models import Membership, Workspace, WorkspaceAPIKey
from workspaces.utils import set_current_user


@pytest.fixture(autouse=True)
def run_around_tests():
    set_current_user(None)


@pytest.fixture
def create_workspace(name=None):
    return Workspace.objects.create(name=uuid.uuid4() if name is None else name)


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


@pytest.fixture
def api_key(create_user, create_workspace):
    user = create_user()
    api_key, key = WorkspaceAPIKey.objects.create_key(
        name="ContentAP-tests", workspace=create_workspace, created_by=user
    )
    return key


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


class TestWorkspacesUserAuth:
    @pytest.mark.django_db
    def test_get_workspaces(self, auto_login_user):
        client, user, workspace = auto_login_user()
        url = reverse("workspaces:workspaces-list")
        response = client.get(url)
        assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
        workspaces = list(response.json())
        assert len(workspaces) == 1

    @pytest.mark.django_db
    def test_get_workspaces_no_membership(self, auto_login_user):
        client, user, workspace = auto_login_user()
        Workspace.objects.create(name="abc2")
        url = reverse("workspaces:workspaces-list")
        response = client.get(url)
        assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
        workspaces = list(response.json())
        assert len(workspaces) == 1


class TestWorkspacesApiKeyAuth:
    @pytest.mark.django_db
    def test_get_workspaces(self, api_client, api_key):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        url = reverse("workspaces:workspaces-list")
        response = api_client.get(url)
        assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
        workspaces = list(response.json())
        assert len(workspaces) == 1

    @pytest.mark.django_db
    def test_get_workspaces_wrong_key(self, api_client, api_key):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        Workspace.objects.create(name="abc2")
        url = reverse("workspaces:workspaces-list")
        response = api_client.get(url)
        assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
        workspaces = list(response.json())
        assert len(workspaces) == 1


class TestWorkspaceUserAuth:
    @pytest.mark.django_db
    def test_get_workspace(self, auto_login_user):
        client, user, workspace = auto_login_user()
        url = reverse("workspaces:workspaces-detail", kwargs={"pk": str(workspace.id)})
        response = client.get(url)
        assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"

    @pytest.mark.django_db
    def test_get_workspace_no_membership(self, auto_login_user):
        client, user, workspace = auto_login_user()
        workspace2 = Workspace.objects.create(name="abc2")
        url = reverse("workspaces:workspaces-detail", kwargs={"pk": str(workspace2.id)})
        response = client.get(url)
        assert response.status_code == 404, f"verb `get` failed on workspaces with status {response.status_code}"


class TestWorkspaceApiKeyAuth:
    @pytest.mark.django_db
    def test_get_workspace(self, api_client, api_key, create_workspace):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        url = reverse("workspaces:workspaces-detail", kwargs={"pk": str(create_workspace.id)})
        response = api_client.get(url)
        assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"

    @pytest.mark.django_db
    def test_get_workspace_wrong_key(self, api_client, api_key):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        workspace2 = Workspace.objects.create(name="abc2")
        url = reverse("workspaces:workspaces-detail", kwargs={"pk": str(workspace2.id)})
        response = api_client.get(url)
        assert response.status_code == 404, f"verb `get` failed on workspaces with status {response.status_code}"
