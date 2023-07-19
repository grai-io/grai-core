import django.db.utils
import pytest
from django.urls import reverse

from .common import (
    api_client,
    api_key,
    auto_login_user,
    create_edge_with_node_ids,
    create_edge_without_node_ids,
    create_membership,
    create_node,
    create_source,
    create_user,
    create_workspace,
    test_edges,
    test_full_nodes,
    test_nodes,
    test_password,
    test_source,
)


@pytest.mark.django_db
def test_post_edge(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_edge_with_node_ids(api_client, create_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_post_edge_without_ids(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_edge_without_node_ids(api_client, create_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_post_edge_data_soruces(api_key, create_workspace, api_client, test_source):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_edge_with_node_ids(
        api_client,
        create_workspace,
        sources=[
            {
                "id": str(test_source.id),
            }
        ],
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_duplicate_edge_nodes(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    node_id = create_node(api_client, create_workspace).json()["id"]
    with pytest.raises(django.db.utils.IntegrityError):
        response = create_edge_with_node_ids(api_client, create_workspace, source=node_id, destination=node_id)


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
        results = response.json()["results"]
        assert len(results) == 1, f"Wrong number of edges returned in query. Expected 1, got {len(results)}"

    def test_query_by_name_is_correct(self, client, test_edges):
        edge = test_edges[2]
        url = self.get_url_by_name(edge)
        response = client.get(url)
        results = response.json()["results"][0]
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
        result = response.json()["results"]
        assert len(result) == 1, f"Wrong number of edges returned in query. Expected 1, got {len(result)}"

    def test_query_by_source_destination_is_correct(self, client, test_edges):
        edge = test_edges[2]
        url = self.get_url_by_source_destination(edge)
        response = client.get(url)
        result = response.json()["results"][0]
        assert result["name"] == edge["name"]
        assert result["namespace"] == edge["namespace"]
        assert result["id"] == edge["id"]

    def test_filter_by_source_name(self, client, test_edges, test_source):
        edge = test_edges[0]
        url = f"{reverse('graph:edges-list')}?source_name={test_source.name}"
        response = client.get(url, content_type="application/json")
        assert response.status_code == 200, response


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
    def test_no_auth(self, auto_login_user, test_nodes, create_workspace):
        client, user = auto_login_user()
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
