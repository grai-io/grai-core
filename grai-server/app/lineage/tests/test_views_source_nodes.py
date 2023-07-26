import uuid

import pytest
from django.urls import reverse

from lineage.models import Source

from .common import (
    api_client,
    api_key,
    auto_login_user,
    create_membership,
    create_node,
    create_user,
    create_workspace,
    test_full_nodes,
    test_node,
    test_nodes,
    test_password,
    test_source,
)


@pytest.mark.django_db
def test_get_source_nodes(auto_login_user, test_source):
    client, user = auto_login_user()
    url = reverse("graph:source-nodes-list", kwargs={"source_pk": test_source.id})
    response = client.get(url)
    assert response.status_code == 200, f"verb `get` failed on {url} with status {response.status_code}"


@pytest.mark.django_db
def test_post_node(api_key, api_client, test_source):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {"name": str(uuid.uuid4()), "namespace": "default", "metadata": "{}"}

    url = reverse("graph:source-nodes-list", kwargs={"source_pk": test_source.id})
    response = api_client.post(url, args)

    assert response.status_code == 201


@pytest.mark.django_db
def test_post_node_upsert(api_key, api_client, test_source, test_node):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {
        "name": test_node.name,
        "namespace": test_node.namespace,
        "metadata": "{}",
    }

    url = reverse("graph:source-nodes-list", kwargs={"source_pk": test_source.id})
    response = api_client.post(url, args)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_node_upsert_new_source(api_key, api_client, test_node, create_workspace):
    source = Source.objects.create(workspace=create_workspace, name=str(uuid.uuid4()))

    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {
        "name": test_node.name,
        "namespace": test_node.namespace,
        "metadata": "{}",
    }

    url = reverse("graph:source-nodes-list", kwargs={"source_pk": source.id})
    response = api_client.post(url, args)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_node_update(api_key, api_client, test_source, test_node):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    args = {
        "name": test_node.name,
        "namespace": test_node.namespace,
        "metadata": "{}",
    }

    url = reverse(
        "graph:source-nodes-detail",
        kwargs={"source_pk": test_source.id, "pk": test_node.id},
    )
    response = api_client.put(url, args)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_node_delete(api_key, api_client, test_source, test_node):
    api_client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")

    url = reverse(
        "graph:source-nodes-detail",
        kwargs={"source_pk": test_source.id, "pk": test_node.id},
    )
    response = api_client.delete(url)

    assert response.status_code == 204
