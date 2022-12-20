import json
import uuid
from itertools import product

import django.db.utils
import pytest
from django.test import Client
from django.test.client import RequestFactory
from django.urls import reverse
from lineage.models import Edge, Node
from lineage.urls import app_name
from rest_framework.test import APIClient, force_authenticate
from rest_framework_api_key.models import APIKey
from users.models import User


def create_node(client, name=None, namespace="default", data_source="test"):
    args = {
        "name": uuid.uuid4() if name is None else name,
        "namespace": namespace,
        "data_source": data_source,
    }

    url = reverse("graph:nodes-list")
    response = client.post(url, args)
    return response


def create_edge_with_node_ids(
    client, source=None, destination=None, data_source="test", **kwargs
):
    if source is None:
        source = create_node(client).json()["id"]
    if destination is None:
        destination = create_node(client).json()["id"]
    args = {
        "data_source": data_source,
        "source": source,
        "destination": destination,
        "namespace": "default",
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
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
            client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


actions = ["list"]
route_prefixes = ["nodes", "edges"]
targets = [
    (f"{app_name}:{prefix}-{action}", 200)
    for prefix, action in product(route_prefixes, actions)
]


@pytest.mark.parametrize("url_name,status", targets)
@pytest.mark.django_db
def test_get_endpoints(auto_login_user, url_name, status):
    client, user = auto_login_user()
    url = reverse(url_name)
    response = client.get(url)
    assert (
        response.status_code == status
    ), f"verb `get` failed on {url} with status {response.status_code}"


@pytest.mark.django_db
def test_post_node(auto_login_user):
    client, user = auto_login_user()
    response = create_node(client)
    assert response.status_code == 201


@pytest.mark.django_db
def test_patch_node(auto_login_user):
    client, user = auto_login_user()
    response = create_node(client)
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
    result = client.patch(url, json.dumps(args), content_type="application/json")
    assert result.status_code == 200
    result = result.json()
    assert all(result[key] == value for key, value in args.items())


@pytest.mark.django_db
def test_delete_node(auto_login_user):
    client, user = auto_login_user()
    response = create_node(client)
    assert response.status_code == 201
    node_id = response.json()["id"]

    url = reverse("graph:nodes-detail", kwargs={"pk": node_id})
    result = client.delete(url)
    assert result.status_code == 204

    result = client.get(reverse("graph:nodes-detail", kwargs={"pk": node_id}))
    assert result.status_code == 404


@pytest.mark.django_db
def test_post_edge(auto_login_user):
    client, user = auto_login_user()
    response = create_edge_with_node_ids(client)
    assert response.status_code == 201


# @pytest.mark.django_db
# def test_post_edge_without_node_ids(auto_login_user):
#     client, user = auto_login_user()
#     response = create_edge_without_node_ids(client)
#     assert response.status_code == 201, f"Failed to create edge using node name/namespace information. Got status code {response.status_code} and {response.json()}"


@pytest.mark.django_db
def test_duplicate_nodes(auto_login_user):
    client, user = auto_login_user()
    name = "test_node"
    create_node(client, name)
    with pytest.raises(django.db.utils.IntegrityError):
        response = create_node(client, name)


@pytest.mark.django_db
def test_duplicate_edge_nodes(auto_login_user):
    client, user = auto_login_user()
    node_id = create_node(client).json()["id"]
    with pytest.raises(django.db.utils.IntegrityError):
        response = create_edge_with_node_ids(
            client, source=node_id, destination=node_id
        )


@pytest.fixture
def api_key():
    api_key, key = APIKey.objects.create_key(name=str(uuid.uuid4()))
    return key


class TestNodeUserAuth:
    def test_password_auth(self, db, client, create_user, test_password):
        user = create_user()
        client.login(username=user.username, password=test_password)
        response = create_node(client)
        assert response.status_code == 201

    def test_incorrect_password_auth(self, db, client, create_user):
        user = create_user()
        client.login(username=user.username, password="wrong_password")
        response = create_node(client)
        assert response.status_code == 403

    def test_no_auth(self, db, client, create_user):
        user = create_user()
        response = create_node(client)
        assert response.status_code == 403

    def test_token_auth(self, db, client, create_user):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token.key}")
        response = create_node(client)
        assert response.status_code == 201

    def test_invalid_token_auth(self, db, client, create_user):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token wrong_token")
        response = create_node(client)
        assert response.status_code == 403

    def test_api_key_auth(self, db, client, create_user, api_key):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        response = create_node(client)
        assert response.status_code == 201

    def test_invalid_api_key_auth(self, db, client, create_user, api_key):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Api-Key wrong_api_key")
        response = create_node(client)
        assert response.status_code == 403


@pytest.fixture
def test_nodes(db, client, auto_login_user, n=2):
    client, user = auto_login_user()
    nodes = [create_node(client).json()["id"] for i in range(n)]
    return nodes


@pytest.fixture
def test_full_nodes(auto_login_user):
    client, user = auto_login_user()
    nodes = [create_node(client).json() for i in range(4)]
    return nodes


@pytest.fixture
def test_edges(auto_login_user, test_full_nodes):
    client, user = auto_login_user()
    edges = []
    for source, destination in zip(test_full_nodes, test_full_nodes[1:]):
        edge = create_edge_with_node_ids(
            client, source=source["id"], destination=destination["id"]
        )
        edges.append(edge.json())
    return edges


class TestNodeWithFilter:
    def get_url_by_name(self, node):
        return f"{reverse('graph:nodes-list')}?name={node['name']}&namespace={node['namespace']}"

    def get_url_by_id(self, node):
        return f"{reverse('graph:nodes-list')}{node['id']}/"

    def test_query_by_name(self, client, test_full_nodes):
        node = test_full_nodes[0]
        url = self.get_url_by_name(node)
        response = client.get(url)
        assert response.status_code == 200, response

    def test_query_by_name_is_unique(self, client, test_full_nodes):
        node = test_full_nodes[1]
        url = self.get_url_by_name(node)
        response = client.get(url)
        results = response.json()
        assert (
            len(results) == 1
        ), f"Wrong number of nodes returned in query. Expected 1, got {len(results)}"

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
        assert isinstance(
            result, dict
        ), f"Expected only a single dictionary got {type(result)}"

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
        assert (
            len(results) == 1
        ), f"Wrong number of edges returned in query. Expected 1, got {len(results)}"

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
        assert isinstance(
            result, dict
        ), f"Expected only a single dictionary got {type(result)}"

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
        assert (
            len(result) == 1
        ), f"Wrong number of edges returned in query. Expected 1, got {len(results)}"

    def test_query_by_source_destination_is_correct(self, client, test_edges):
        edge = test_edges[2]
        url = self.get_url_by_source_destination(edge)
        response = client.get(url)
        result = response.json()[0]
        assert result["name"] == edge["name"]
        assert result["namespace"] == edge["namespace"]
        assert result["id"] == edge["id"]


class TestEdgeUserAuth:
    def test_password_auth(self, db, client, auto_login_user, test_nodes):
        client, user = auto_login_user()
        response = create_edge_with_node_ids(client, *test_nodes)
        assert response.status_code == 201

    def test_incorrect_password_auth(self, db, client, create_user, test_nodes):
        user = create_user()
        client.logout()
        client.login(username=user.username, password="wrong_password")
        response = create_edge_with_node_ids(client, *test_nodes)
        assert response.status_code == 403

    def test_no_auth(self, db, client, create_user, test_nodes):
        client.logout()
        response = create_edge_with_node_ids(client, *test_nodes)
        assert response.status_code == 403

    def test_token_auth(self, db, create_user, *test_nodes):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token.key}")
        response = create_edge_with_node_ids(client, *test_nodes)
        assert response.status_code == 201

    def test_invalid_token_auth(self, db, create_user, test_nodes):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token wrong_token")
        response = create_edge_with_node_ids(client, *test_nodes)
        assert response.status_code == 403

    def test_api_key_auth(self, db, api_key, test_nodes):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        response = create_edge_with_node_ids(client, *test_nodes)
        assert response.status_code == 201

    def test_invalid_api_key_auth(self, db, api_key, test_nodes):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Api-Key wrong_api_key")
        response = create_edge_with_node_ids(client, *test_nodes)
        assert response.status_code == 403
