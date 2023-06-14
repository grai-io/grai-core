import uuid
from lineage.graph_tasks import cache_node, cache_edge
import pytest
from workspaces.models import Organisation, Workspace
from lineage.models import Edge, Node


@pytest.fixture
def test_organisation():
    return Organisation.objects.create(name=str(uuid.uuid4()))


@pytest.fixture
def test_workspace(test_organisation):
    return Workspace.objects.create(name=str(uuid.uuid4()), organisation=test_organisation)


@pytest.fixture
def test_node(test_workspace):
    return Node.objects.create(workspace=test_workspace, name=str(uuid.uuid4()))


@pytest.fixture
def test_source_node(test_workspace):
    return Node.objects.create(workspace=test_workspace, name=str(uuid.uuid4()))


@pytest.fixture
def test_destination_node(test_workspace):
    return Node.objects.create(workspace=test_workspace, name=str(uuid.uuid4()))


@pytest.fixture
def test_edge(test_workspace, test_source_node, test_destination_node):
    return Edge.objects.create(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        source=test_source_node,
        destination=test_destination_node,
    )


@pytest.mark.django_db
def test_cache_node(test_node):
    cache_node(test_node.id)


@pytest.mark.django_db
def test_cache_node_delete(test_node):
    cache_node(test_node.id, delete=True)


@pytest.mark.django_db
def test_cache_edge(test_edge):
    cache_edge(test_edge.id)


@pytest.mark.django_db
def test_cache_edge_delete(test_edge):
    cache_edge(test_edge.id, delete=True)
