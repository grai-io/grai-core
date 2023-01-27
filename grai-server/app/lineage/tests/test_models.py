import datetime
import uuid

# Create your tests here.
import pytest
from django.test import TestCase

from lineage.models import Edge, Node
from workspaces.models import Workspace


@pytest.mark.django_db
def test_node_created():
    workspace = Workspace.objects.create(name="W1")

    node = Node.objects.create(namespace="temp", name="a", data_source="test", workspace=workspace)

    assert node.id == uuid.UUID(str(node.id))
    assert node.name == "a"
    assert node.namespace == "temp"
    assert node.data_source == "test"
    assert node.display_name == "a"
    assert isinstance(node.metadata, dict) and len(node.metadata.keys()) == 0
    assert node.is_active
    assert isinstance(node.created_at, datetime.datetime)
    assert isinstance(node.updated_at, datetime.datetime)


@pytest.mark.django_db
def test_node_created_from_load():
    workspace = Workspace.objects.create(name="W1")

    node = Node.objects.create(namespace="temp2", name="abc", data_source="test", workspace=workspace)
    nodes = list(Node.objects.filter(namespace="temp2", name="abc").all())
    assert len(nodes) == 1
    node2 = nodes[0]
    attrs = ["id", "name", "namespace", "data_source", "display_name"]
    for attr in attrs:
        assert getattr(node, attr) == getattr(node2, attr)


@pytest.mark.django_db
def test_edge_created():
    workspace = Workspace.objects.create(name="W1")

    node_a = Node.objects.create(
        namespace="default",
        name="node_a",
        data_source="node_source",
        workspace=workspace,
    )
    node_b = Node.objects.create(
        namespace="default",
        name="node_b",
        data_source="node_source",
        workspace=workspace,
    )
    edge = Edge.objects.create(
        data_source="edge_source",
        source_id=node_a.id,
        destination_id=node_b.id,
        workspace=workspace,
    )

    assert edge.id == uuid.UUID(str(edge.id))
    assert edge.data_source == "edge_source"
    assert edge.is_active
    assert isinstance(edge.metadata, dict) and len(edge.metadata.keys()) == 0
    assert isinstance(edge.created_at, datetime.datetime)
    assert isinstance(edge.updated_at, datetime.datetime)

    assert edge.source == node_a
    assert edge.destination == node_b
