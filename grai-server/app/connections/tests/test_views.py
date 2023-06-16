import uuid

import pytest
from django.urls import reverse
from django_multitenant.utils import set_current_tenant

from connections.models import Connection, Connector
from workspaces.models import Membership, Organisation, Workspace, WorkspaceAPIKey
from lineage.models import Source


@pytest.fixture
def create_organisation(name: str = None):
    return Organisation.objects.create(name=str(uuid.uuid4()) if name is None else name)


@pytest.fixture
def create_workspace(create_organisation, name: str = None):
    return Workspace.objects.create(
        name=str(uuid.uuid4()) if name is None else name,
        organisation=create_organisation,
    )


@pytest.fixture
def create_workspace2(create_organisation, name: str = None):
    return Workspace.objects.create(
        name=str(uuid.uuid4()) if name is None else name,
        organisation=create_organisation,
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


@pytest.fixture
def test_connector():
    connector = Connector.objects.create(name=str(uuid.uuid4()))

    return connector


@pytest.fixture
def test_source(create_workspace):
    source = Source.objects.create(name=str(uuid.uuid4()), workspace=create_workspace)

    return source


@pytest.fixture
def test_connection(test_connector, create_workspace, test_source):
    connection = Connection.objects.create(
        name=str(uuid.uuid4()),
        connector=test_connector,
        workspace=create_workspace,
        source=test_source,
    )

    return connection


@pytest.mark.django_db
class TestConnectors:
    def test_get_connectors(self, auto_login_user, test_connector):
        set_current_tenant(None)
        client, user, workspace = auto_login_user()
        url = reverse("connections:connectors-list")
        response = client.get(url)
        assert response.status_code == 200, f"verb `get` failed on connectors with status {response.status_code}"
        connectors = list(response.json()["results"])
        assert len(connectors) > 0

    def test_get_connectors_filter_by_active(self, auto_login_user, test_connector):
        client, user, workspace = auto_login_user()
        url = reverse("connections:connectors-list")
        response = client.get(f"{url}?is_active=True")
        assert response.status_code == 200, f"verb `get` failed on connectors with status {response.status_code}"
        connectors = list(response.json()["results"])
        assert len(connectors) > 0

    def test_get_connectors_filter_by_active_false(self, auto_login_user, test_connector):
        client, user, workspace = auto_login_user()
        url = reverse("connections:connectors-list")
        response = client.get(f"{url}?is_active=False")
        assert response.status_code == 200, f"verb `get` failed on connectors with status {response.status_code}"
        connectors = list(response.json()["results"])
        assert len(connectors) == 0

    def test_get_connector(self, auto_login_user, test_connector):
        client, user, workspace = auto_login_user()
        url = reverse("connections:connectors-detail", kwargs={"pk": str(test_connector.id)})
        response = client.get(url)
        assert response.status_code == 200, f"verb `get` failed on connectors with status {response.status_code}"
        assert response.json()["name"] == test_connector.name


@pytest.mark.django_db
class TestConnections:
    def test_get_connections(self, auto_login_user, test_connection):
        client, user, workspace = auto_login_user()
        url = reverse("connections:connections-list")
        response = client.get(url)
        assert response.status_code == 200, f"verb `get` failed on connections with status {response.status_code}"
        connections = list(response.json()["results"])
        assert len(connections) == 1
        assert connections[0]["name"] == test_connection.name

    def test_get_connections_filter_by_active(self, auto_login_user, test_connection):
        client, user, workspace = auto_login_user()
        url = reverse("connections:connections-list")
        response = client.get(f"{url}?is_active=True")
        assert response.status_code == 200, f"verb `get` failed on connections with status {response.status_code}"
        connections = list(response.json()["results"])
        assert len(connections) == 1
        assert connections[0]["name"] == test_connection.name

    def test_get_connectionss_filter_by_active_false(self, auto_login_user, test_connection):
        client, user, workspace = auto_login_user()
        url = reverse("connections:connections-list")
        response = client.get(f"{url}?is_active=False")
        assert response.status_code == 200, f"verb `get` failed on connections with status {response.status_code}"
        connections = list(response.json()["results"])
        assert len(connections) == 0

    def test_get_connections(self, auto_login_user, test_connection):
        client, user, workspace = auto_login_user()
        url = reverse("connections:connections-detail", kwargs={"pk": str(test_connection.id)})
        response = client.get(url)
        assert response.status_code == 200, f"verb `get` failed on connections with status {response.status_code}"
        assert response.json()["name"] == test_connection.name
