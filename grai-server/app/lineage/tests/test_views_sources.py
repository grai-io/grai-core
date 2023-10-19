import json

import pytest
from django.urls import reverse

from .conftest import create_source


@pytest.mark.django_db
def test_post_source(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_source(api_client, create_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_patch_source(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_source(api_client, create_workspace)
    assert response.status_code == 201
    source_id = response.json()["id"]

    url = reverse("graph:sources-detail", kwargs={"pk": source_id})
    args = {
        "name": "strisdfsdfng",
    }
    result = api_client.patch(url, json.dumps(args), content_type="application/json")
    assert result.status_code == 200
    result = result.json()
    assert all(result[key] == value for key, value in args.items())


@pytest.mark.django_db
def test_delete_source(api_key, create_workspace, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_source(api_client, create_workspace)
    assert response.status_code == 201
    source_id = response.json()["id"]

    url = reverse("graph:sources-detail", kwargs={"pk": source_id})
    result = api_client.delete(url)
    assert result.status_code == 204

    result = api_client.get(reverse("graph:sources-detail", kwargs={"pk": source_id}))
    assert result.status_code == 404


@pytest.fixture
def test_full_sources(auto_login_user, create_workspace):
    client, user = auto_login_user()
    sources = [create_source(client, create_workspace).json() for i in range(4)]
    return sources


class TestSourceWithFilter:
    def get_url_by_name(self, source):
        return f"{reverse('graph:sources-list')}?name={source['name']}"

    def get_url_by_id(self, source):
        return f"{reverse('graph:sources-list')}{source['id']}/"

    @pytest.mark.django_db
    def test_query_by_name(self, test_full_sources, auto_login_user):
        client, user = auto_login_user()
        source = test_full_sources[0]
        url = self.get_url_by_name(source)
        response = client.get(url)
        print(response)
        assert response.status_code == 200, response

    @pytest.mark.django_db
    def test_query_by_name_is_unique(self, client, test_full_sources, auto_login_user):
        client, user = auto_login_user()
        source = test_full_sources[1]
        url = self.get_url_by_name(source)
        response = client.get(url)
        results = response.json()["results"]
        assert len(results) == 1, f"Wrong number of sources returned in query. Expected 1, got {len(results)}"

    def test_query_by_name_is_correct(self, client, test_full_sources):
        source = test_full_sources[2]
        url = self.get_url_by_name(source)
        response = client.get(url)
        results = response.json()["results"][0]
        assert results["name"] == source["name"]
        assert results["id"] == source["id"]

    def test_query_by_id(self, client, test_full_sources):
        source = test_full_sources[0]
        url = self.get_url_by_id(source)
        response = client.get(url, content_type="application/json")
        assert response.status_code == 200, response

    def test_query_by_id_is_unique(self, client, test_full_sources):
        source = test_full_sources[1]
        url = self.get_url_by_id(source)
        response = client.get(url, content_type="application/json")
        result = response.json()
        assert isinstance(result, dict), f"Expected only a single dictionary got {type(result)}"

    def test_query_by_id_is_correct(self, client, test_full_sources):
        source = test_full_sources[2]
        url = self.get_url_by_id(source)
        response = client.get(url)
        result = response.json()
        assert result["name"] == source["name"]
        assert result["id"] == source["id"]
