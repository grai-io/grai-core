import json
import uuid
from itertools import product

import django.db.utils
import pytest
from django.urls import reverse

from lineage.models import Node
from lineage.urls import app_name
from workspaces.models import Membership, Organisation, Workspace, WorkspaceAPIKey


def create_node(client, workspace, name=None, namespace="default", data_source="test"):
    args = {
        "name": uuid.uuid4() if name is None else name,
        "namespace": namespace,
        "data_source": data_source,
        "workspace": str(workspace.id),
    }

    url = reverse("graph:nodes-list")
    response = client.post(url, args, SERVER_NAME="localhost")
    return response


def create_edge_with_node_ids(client, workspace, source=None, destination=None, data_source="test", **kwargs):
    if source is None:
        source = create_node(client, workspace).json()["id"]
    if destination is None:
        destination = create_node(client, workspace).json()["id"]
    args = {
        "data_source": data_source,
        "source": source,
        "destination": destination,
        "namespace": "default",
        "workspace": str(workspace.id),
    }

    url = reverse("graph:edges-list")
    response = client.post(url, args, **kwargs)
    return response


# def create_edge_without_node_ids(client, source=None, destination=None, data_source="test", **kwargs):
#     if source is None:
#         source = create_node(client).json()
#     if destination is None:
#         destination = create_node(client).json()
#     args = {"data_source": data_source,
#             "source": {k: source[k] for k in ['name', 'namespace']},
#             "destination": {k: destination[k] for k in ['name', 'namespace']}}
#
#     print(args)
#     url = reverse("graph:edges-list")
#     response = client.post(url, args, **kwargs)
#     print(response.request.d)
#     return response


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
        return client, user

    return make_auto_login


actions = ["list"]
route_prefixes = ["nodes", "edges"]
targets = [(f"{app_name}:{prefix}-{action}", 200) for prefix, action in product(route_prefixes, actions)]


@pytest.mark.parametrize("url_name,status", targets)
@pytest.mark.django_db
def test_get_endpoints(auto_login_user, url_name, status):
    client, user = auto_login_user()
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == status, f"verb `get` failed on {url} with status {response.status_code}"


@pytest.mark.django_db
def test_post_node(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_node(api_client, create_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_post_node_second_workspace(auto_login_user):
    client, user = auto_login_user()

    organisation = Organisation.objects.create(name=str(uuid.uuid4()))

    first_workspace = Workspace.objects.create(name="first", organisation=organisation)
    second_workspace = Workspace.objects.create(name="second", organisation=organisation)

    Membership.objects.create(role="admin", user=user, workspace=first_workspace)
    Membership.objects.create(role="admin", user=user, workspace=second_workspace)

    response = create_node(client, first_workspace)
    assert response.status_code == 201
    id = response.json()["id"]
    node = Node.objects.get(id=id)
    assert str(node.workspace_id) == str(first_workspace.id)

    response = create_node(client, second_workspace)
    assert response.status_code == 201
    id = response.json()["id"]
    node = Node.objects.get(id=id)
    assert str(node.workspace_id) == str(second_workspace.id)


@pytest.mark.django_db
def test_patch_node(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_node(api_client, create_workspace)
    assert response.status_code == 201
    node_id = response.json()["id"]

    url = reverse("graph:nodes-detail", kwargs={"pk": node_id})
    args = {
        "namespace": "string",
        "name": "strisdfsdfng",
        "display_name": "string",
        "data_source": "string",
        "metadata": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string",
        },
        "is_active": False,
    }
    result = api_client.patch(url, json.dumps(args), content_type="application/json")
    assert result.status_code == 200
    result = result.json()
    assert all(result[key] == value for key, value in args.items())


@pytest.mark.django_db
def test_delete_node(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_node(api_client, create_workspace)
    assert response.status_code == 201
    node_id = response.json()["id"]

    url = reverse("graph:nodes-detail", kwargs={"pk": node_id})
    result = api_client.delete(url)
    assert result.status_code == 204

    result = api_client.get(reverse("graph:nodes-detail", kwargs={"pk": node_id}))
    assert result.status_code == 404


@pytest.mark.django_db
def test_post_edge(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_edge_with_node_ids(api_client, create_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_duplicate_nodes(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    name = "test_node"
    create_node(api_client, create_workspace, name)
    with pytest.raises(django.db.utils.IntegrityError):
        response = create_node(api_client, create_workspace, name)


@pytest.mark.django_db
def test_duplicate_edge_nodes(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    node_id = create_node(api_client, create_workspace).json()["id"]
    with pytest.raises(django.db.utils.IntegrityError):
        response = create_edge_with_node_ids(api_client, create_workspace, source=node_id, destination=node_id)


@pytest.fixture
def create_workspace(name=None):
    organisation = Organisation.objects.create(name="Test Organisation3")

    return Workspace.objects.create(name=uuid.uuid4() if name is None else name, organisation=organisation)


@pytest.fixture
def create_membership(create_workspace):
    def make_membership(user):
        membership = Membership.objects.create(role="admin", user=user, workspace=create_workspace)
        return membership, create_workspace

    return make_membership


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


class TestNodeUserAuth:
    @pytest.mark.django_db
    def test_password_auth(self, auto_login_user, create_workspace):
        client, user = auto_login_user()
        response = create_node(client, create_workspace)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_incorrect_password_auth(self, client, create_user, create_workspace):
        user = create_user()
        client.login(username=user.username, password="wrong_password")
        response = create_node(client, create_workspace)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_no_auth(self, client, create_workspace):
        client.logout()
        response = create_node(client, create_workspace)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_api_key_auth(self, create_workspace, api_client, api_key):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        response = create_node(api_client, create_workspace)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_invalid_api_key_auth(self, create_workspace, api_client):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key wrong_api_key")
        response = create_node(api_client, create_workspace)
        assert response.status_code == 403


@pytest.fixture
def test_nodes(api_key, create_workspace, api_client, n=2):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    nodes = [create_node(api_client, create_workspace).json()["id"] for i in range(n)]
    return nodes


@pytest.fixture
def test_full_nodes(auto_login_user, create_workspace):
    client, user = auto_login_user()
    nodes = [create_node(client, create_workspace).json() for i in range(4)]
    return nodes


@pytest.fixture
def test_edges(auto_login_user, test_full_nodes, create_workspace):
    client, user = auto_login_user()
    edges = []
    for source, destination in zip(test_full_nodes, test_full_nodes[1:]):
        edge = create_edge_with_node_ids(
            client,
            workspace=create_workspace,
            source=source["id"],
            destination=destination["id"],
        )
        edges.append(edge.json())
    return edges


class TestNodeWithFilter:
    def get_url_by_name(self, node):
        return f"{reverse('graph:nodes-list')}?name={node['name']}&namespace={node['namespace']}"

    def get_url_by_id(self, node):
        return f"{reverse('graph:nodes-list')}{node['id']}/"

    @pytest.mark.django_db
    def test_query_by_name(self, test_full_nodes, auto_login_user):
        client, user = auto_login_user()
        node = test_full_nodes[0]
        url = self.get_url_by_name(node)
        response = client.get(url)
        print(response)
        assert response.status_code == 200, response

    @pytest.mark.django_db
    def test_query_by_name_is_unique(self, client, test_full_nodes, auto_login_user):
        client, user = auto_login_user()
        node = test_full_nodes[1]
        url = self.get_url_by_name(node)
        response = client.get(url)
        results = response.json()
        assert len(results) == 1, f"Wrong number of nodes returned in query. Expected 1, got {len(results)}"

    def test_query_by_name_is_correct(self, client, test_full_nodes):
        node = test_full_nodes[2]
        url = self.get_url_by_name(node)
        response = client.get(url)
        results = response.json()[0]
        assert results["name"] == node["name"]
        assert results["namespace"] == node["namespace"]
        assert results["id"] == node["id"]

    def test_query_by_id(self, client, test_full_nodes):
        node = test_full_nodes[0]
        url = self.get_url_by_id(node)
        response = client.get(url, content_type="application/json")
        assert response.status_code == 200, response

    def test_query_by_id_is_unique(self, client, test_full_nodes):
        node = test_full_nodes[1]
        url = self.get_url_by_id(node)
        response = client.get(url, content_type="application/json")
        result = response.json()
        assert isinstance(result, dict), f"Expected only a single dictionary got {type(result)}"

    def test_query_by_id_is_correct(self, client, test_full_nodes):
        node = test_full_nodes[2]
        url = self.get_url_by_id(node)
        response = client.get(url)
        result = response.json()
        assert result["name"] == node["name"]
        assert result["namespace"] == node["namespace"]
        assert result["id"] == node["id"]


class TestEdgesWithFilter:
    def get_url_by_name(self, obj):
        return f"{reverse('graph:edges-list')}?name={obj['name']}&namespace={obj['namespace']}"

    def get_url_by_source_destination(self, obj):
        return f"{reverse('graph:edges-list')}?source={obj['source']}&destination={obj['destination']}"

    def get_url_by_id(self, obj):
        return f"{reverse('graph:edges-list')}{obj['id']}/"

    def test_query_by_name(self, client, test_edges):
        edge = test_edges[0]
        url = self.get_url_by_name(edge)
        response = client.get(url)
        assert response.status_code == 200, response

    def test_query_by_name_is_unique(self, client, test_edges):
        edge = test_edges[1]
        url = self.get_url_by_name(edge)
        response = client.get(url)
        results = response.json()
        assert len(results) == 1, f"Wrong number of edges returned in query. Expected 1, got {len(results)}"

    def test_query_by_name_is_correct(self, client, test_edges):
        edge = test_edges[2]
        url = self.get_url_by_name(edge)
        response = client.get(url)
        results = response.json()[0]
        assert results["name"] == edge["name"]
        assert results["namespace"] == edge["namespace"]
        assert results["id"] == edge["id"]

    def test_query_by_id(self, client, test_edges):
        edge = test_edges[0]
        url = self.get_url_by_id(edge)
        response = client.get(url, content_type="application/json")
        assert response.status_code == 200, response

    def test_query_by_id_is_unique(self, client, test_edges):
        edge = test_edges[1]
        url = self.get_url_by_id(edge)
        response = client.get(url, content_type="application/json")
        result = response.json()
        assert isinstance(result, dict), f"Expected only a single dictionary got {type(result)}"

    def test_query_by_id_is_correct(self, client, test_edges):
        edge = test_edges[2]
        url = self.get_url_by_id(edge)
        response = client.get(url)
        result = response.json()
        assert result["name"] == edge["name"]
        assert result["namespace"] == edge["namespace"]
        assert result["id"] == edge["id"]

    def test_query_by_source_destination(self, client, test_edges):
        edge = test_edges[0]
        url = self.get_url_by_source_destination(edge)
        response = client.get(url, content_type="application/json")
        assert response.status_code == 200, response

    def test_query_by_source_destination_is_unique(self, client, test_edges):
        edge = test_edges[1]
        url = self.get_url_by_source_destination(edge)
        response = client.get(url, content_type="application/json")
        result = response.json()
        assert len(result) == 1, f"Wrong number of edges returned in query. Expected 1, got {len(result)}"

    def test_query_by_source_destination_is_correct(self, client, test_edges):
        edge = test_edges[2]
        url = self.get_url_by_source_destination(edge)
        response = client.get(url)
        result = response.json()[0]
        assert result["name"] == edge["name"]
        assert result["namespace"] == edge["namespace"]
        assert result["id"] == edge["id"]


class TestEdgeUserAuth:
    @pytest.mark.django_db
    def test_password_auth(self, auto_login_user, test_nodes, create_workspace, test_password):
        client, user = auto_login_user()
        client.login(user=user.username, password=test_password)
        response = create_edge_with_node_ids(client, create_workspace, *test_nodes)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_incorrect_password_auth(self, client, create_user, create_workspace, test_nodes):
        user = create_user()
        client.login(username=user.username, password="wrong_password")
        response = create_edge_with_node_ids(client, create_workspace, *test_nodes)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_no_auth(self, client, test_nodes, create_workspace):
        client.logout()
        response = create_edge_with_node_ids(client, create_workspace, *test_nodes)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_api_key_auth(self, api_key, create_workspace, test_nodes, api_client):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        response = create_edge_with_node_ids(api_client, create_workspace, *test_nodes)
        assert response.status_code == 201

    def test_invalid_token_auth(self, test_nodes, api_client, create_workspace):
        api_client.credentials(HTTP_AUTHORIZATION=f"Token wrong_token")
        response = create_edge_with_node_ids(api_client, create_workspace, *test_nodes)
        assert response.status_code == 403

    def test_api_key_auth(self, api_key, test_nodes, api_client, create_workspace):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        response = create_edge_with_node_ids(api_client, create_workspace, *test_nodes)
        assert response.status_code == 201

    def test_invalid_api_key_auth(self, test_nodes, api_client, create_workspace):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key wrong_api_key")
        response = create_edge_with_node_ids(api_client, create_workspace, *test_nodes)
        assert response.status_code == 403
