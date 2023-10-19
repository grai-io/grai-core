import uuid

import pytest
from django.urls import reverse

from lineage.models import Source


@pytest.mark.django_db
def test_get_source_edges(auto_login_user, test_source):
    client, user = auto_login_user()
    url = reverse("graph:source-edges-list", kwargs={"source_pk": test_source.id})
    response = client.get(url)
    assert response.status_code == 200, f"verb `get` failed on {url} with status {response.status_code}"


@pytest.mark.django_db
def test_post_edge(api_key, api_client, test_source, test_source_node, test_node):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {
        "name": str(uuid.uuid4()),
        "namespace": "default",
        "metadata": {},
        "source": test_source_node.id,
        "destination": test_node.id,
    }

    url = reverse("graph:source-edges-list", kwargs={"source_pk": test_source.id})
    response = api_client.post(url, args, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_post_edge_name_namespace(api_key, api_client, test_source, test_source_node, test_node):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {
        "name": str(uuid.uuid4()),
        "namespace": "default",
        "metadata": {},
        "source": {
            "namespace": test_source_node.namespace,
            "name": test_source_node.name,
        },
        "destination": {
            "namespace": test_node.namespace,
            "name": test_node.name,
        },
    }

    url = reverse("graph:source-edges-list", kwargs={"source_pk": test_source.id})
    response = api_client.post(url, args, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_post_edge_upsert(api_key, api_client, test_source, test_edge):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {
        "name": test_edge.name,
        "namespace": test_edge.namespace,
        "metadata": "{}",
        "source": test_edge.source.id,
        "destination": test_edge.destination.id,
    }

    url = reverse("graph:source-edges-list", kwargs={"source_pk": test_source.id})
    response = api_client.post(url, args)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_edge_upsert_new_source(api_key, api_client, test_edge, create_workspace):
    source = Source.objects.create(workspace=create_workspace, name=str(uuid.uuid4()))

    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {
        "name": test_edge.name,
        "namespace": test_edge.namespace,
        "metadata": "{}",
        "source": test_edge.source.id,
        "destination": test_edge.destination.id,
    }

    url = reverse("graph:source-edges-list", kwargs={"source_pk": source.id})
    response = api_client.post(url, args)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_edge_update(api_key, api_client, test_source, test_edge):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {
        "name": test_edge.name,
        "namespace": test_edge.namespace,
        "metadata": "{}",
        "source": test_edge.source.id,
        "destination": test_edge.destination.id,
    }

    url = reverse(
        "graph:source-edges-detail",
        kwargs={"source_pk": test_source.id, "pk": test_edge.id},
    )
    response = api_client.put(url, args)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_edge_delete(api_key, api_client, test_source, test_edge):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")

    url = reverse(
        "graph:source-edges-detail",
        kwargs={"source_pk": test_source.id, "pk": test_edge.id},
    )
    response = api_client.delete(url)

    assert response.status_code == 204
