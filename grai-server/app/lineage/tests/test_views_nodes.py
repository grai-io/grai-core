import json
import uuid
from itertools import product

import django.db.utils
import pytest
from django.urls import reverse

from lineage.models import Node
from lineage.urls import app_name
from workspaces.models import Membership, Organisation, Workspace

from .conftest import api_key, create_node

actions = ["list"]
route_prefixes = ["nodes", "edges", "sources"]
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
def test_post_node_data_sources_by_id(api_key, create_workspace, api_client, test_source):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_node(
        api_client,
        create_workspace,
        sources=[
            {
                "id": test_source.id,
            }
        ],
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_post_node_data_sources_by_name(api_key, create_workspace, api_client, test_source):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_node(
        api_client,
        create_workspace,
        sources=[
            {
                "name": test_source.name,
            }
        ],
    )
    assert response.status_code == 201


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
def test_patch_node_data_sources(api_key, create_workspace, api_client, test_source):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_node(api_client, create_workspace)
    assert response.status_code == 201
    node_id = response.json()["id"]

    url = reverse("graph:nodes-detail", kwargs={"pk": node_id})
    args = {
        "namespace": "string",
        "name": "strisdfsdfng",
        "display_name": "string",
        "metadata": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string",
        },
        "is_active": False,
        "data_sources": [
            {
                "id": str(test_source.id),
                "name": test_source.name,
            }
        ],
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
def test_duplicate_nodes(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    name = "test_node"
    create_node(api_client, create_workspace, name)
    with pytest.raises(django.db.utils.IntegrityError):
        response = create_node(api_client, create_workspace, name)


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
    def test_no_auth(self, auto_login_user, create_workspace):
        client, user = auto_login_user()
        client.logout()
        response = create_node(client, create_workspace)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_no_membership(self, auto_login_user, create_workspace):
        client, user = auto_login_user()

        workspace = Workspace.objects.create(organisation=create_workspace.organisation, name=str(uuid.uuid4()))
        node = Node.objects.create(workspace=workspace, name=str(uuid.uuid4()))

        url = f"{reverse('graph:nodes-list')}{node.id}/"
        response = client.get(url, content_type="application/json")
        assert response.status_code == 404, response

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

    @pytest.mark.django_db
    def test_api_key_no_membership(self, create_workspace, api_client):
        api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        workspace = Workspace.objects.create(name=str(uuid.uuid4()), organisation=create_workspace.organisation)
        response = create_node(api_client, workspace)
        assert response.status_code == 403


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
        results = response.json()["results"]
        assert len(results) == 1, f"Wrong number of nodes returned in query. Expected 1, got {len(results)}"

    def test_query_by_name_is_correct(self, client, test_full_nodes):
        node = test_full_nodes[2]
        url = self.get_url_by_name(node)
        response = client.get(url)
        results = response.json()["results"][0]
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

    @pytest.mark.django_db
    def test_query_by_id_no_membership(self, client):
        organisation = Organisation.objects.create(name=str(uuid.uuid4()))
        workspace = Workspace.objects.create(name=str(uuid.uuid4()), organisation=organisation)
        node = Node.objects.create(name="test", namespace="test", workspace=workspace)
        url = f"{reverse('graph:nodes-list')}{node.id}/"
        response = client.get(url, content_type="application/json")
        assert response.status_code == 403, response

    @pytest.mark.django_db
    def test_filter_by_source_name(self, test_full_nodes, auto_login_user, test_source):
        client, user = auto_login_user()
        node = test_full_nodes[0]
        url = f"{reverse('graph:nodes-list')}?source_name={test_source.name}"
        response = client.get(url)
        print(response)
        assert response.status_code == 200, response
