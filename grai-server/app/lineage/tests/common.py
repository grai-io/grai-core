import json
import uuid

import pytest
from django.urls import reverse

from lineage.models import Edge, Node, Source
from workspaces.models import Membership, Organisation, Workspace, WorkspaceAPIKey


def create_node(client, workspace, name=None, namespace="default", sources=None):
    if sources is None:
        sources = [{"id": create_source(client, workspace).json().get("id")}]

    args = {
        "name": str(uuid.uuid4()) if name is None else name,
        "namespace": namespace,
        "workspace": str(workspace.id),
        "data_sources": sources,
    }

    url = reverse("graph:nodes-list")
    response = client.post(url, args, SERVER_NAME="localhost", format="json")
    return response


def create_source(client, workspace, name=None):
    args = {
        "name": str(uuid.uuid4()) if name is None else name,
        "workspace": str(workspace.id),
    }

    url = reverse("graph:sources-list")
    response = client.post(url, args, SERVER_NAME="localhost")
    return response


def create_edge_with_node_ids(client, workspace, source=None, destination=None, sources=None, **kwargs):
    if source is None:
        source = create_node(client, workspace).json()["id"]
    if destination is None:
        destination = create_node(client, workspace).json()["id"]
    if sources is None:
        sources = [{"id": create_source(client, workspace).json().get("id")}]

    args = {
        "source": source,
        "destination": destination,
        "namespace": "default",
        "workspace": str(workspace.id),
        "data_sources": sources,
    }

    url = reverse("graph:edges-list")
    response = client.post(url, args, format="json", **kwargs)
    return response


def create_edge_without_node_ids(client, workspace, source=None, destination=None, sources=None, **kwargs):
    if source is None:
        source = create_node(client, workspace).json()
    if destination is None:
        destination = create_node(client, workspace).json()
    if sources is None:
        sources = [{"id": create_source(client, workspace).json().get("id")}]

    args = {
        "source": {k: source[k] for k in ["name", "namespace"]},
        "destination": {k: destination[k] for k in ["name", "namespace"]},
        "namespace": "default",
        "workspace": str(workspace.id),
        "data_sources": sources,
    }
    url = reverse("graph:edges-list")

    response = client.post(url, data=json.dumps(args), **kwargs, content_type="application/json")
    return response


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


@pytest.fixture
def create_workspace(name=None):
    organisation = Organisation.objects.create(name=str(uuid.uuid4()))

    return Workspace.objects.create(name=str(uuid.uuid4()) if name is None else name, organisation=organisation)


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


@pytest.fixture
def test_source(create_workspace):
    return Source.objects.create(name=str(uuid.uuid4()), workspace=create_workspace)


@pytest.fixture
def test_node(create_workspace, test_source):
    node = Node.objects.create(name=str(uuid.uuid4()), namespace="default", workspace=create_workspace)

    test_source.nodes.add(node)

    return node


@pytest.fixture
def test_source_node(create_workspace, test_source):
    node = Node.objects.create(name=str(uuid.uuid4()), namespace="default", workspace=create_workspace)

    test_source.nodes.add(node)

    return node


@pytest.fixture
def test_destination_node(create_workspace, test_source):
    node = Node.objects.create(name=str(uuid.uuid4()), namespace="default", workspace=create_workspace)

    test_source.nodes.add(node)

    return node


@pytest.fixture
def test_edge(create_workspace, test_source, test_source_node, test_destination_node):
    edge = Edge.objects.create(
        source=test_source_node,
        destination=test_destination_node,
        namespace="default",
        workspace=create_workspace,
        name=str(uuid.uuid4()),
    )

    test_source.edges.add(edge)

    return edge
