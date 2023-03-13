import datetime
import uuid

# Create your tests here.
import pytest
from django_multitenant.utils import set_current_tenant

from lineage.models import Edge, Node
from workspaces.models import Organisation, Workspace


@pytest.fixture
def create_organisation(name: str = None):
    return Organisation.objects.create(name=uuid.uuid4() if name is None else name)


@pytest.fixture
def create_workspace(create_organisation, name: str = None):
    return Workspace.objects.create(
        name=str(uuid.uuid4()) if name is None else name,
        organisation=create_organisation,
    )


@pytest.mark.django_db
def test_node_created(create_workspace):
    node = Node.objects.create(namespace="temp", name="a", data_source="test", workspace=create_workspace)

    assert node.id == uuid.UUID(str(node.id))
    assert node.name == "a"
    assert node.namespace == "temp"
    assert node.data_source == "test"
    assert node.display_name == "a"
    assert isinstance(node.metadata, dict) and len(node.metadata.keys()) == 0
    assert node.is_active
    assert isinstance(node.created_at, datetime.datetime)
    assert isinstance(node.updated_at, datetime.datetime)
    assert node.search_type() == "Node"
    assert node.table_id() is None


@pytest.mark.django_db
def test_table_table_id(create_workspace):
    metadata = {
        "grai": {
            "node_type": "Table",
        }
    }

    node = Node.objects.create(
        namespace="temp", name="a", data_source="test", workspace=create_workspace, metadata=metadata
    )

    assert node.id == uuid.UUID(str(node.id))
    assert node.name == "a"
    assert node.namespace == "temp"
    assert node.data_source == "test"
    assert node.display_name == "a"
    assert node.is_active
    assert isinstance(node.created_at, datetime.datetime)
    assert isinstance(node.updated_at, datetime.datetime)
    assert node.search_type() == "Table"
    assert node.table_id() == node.id


@pytest.mark.django_db
def test_column_table_id(create_workspace):
    metadata = {
        "grai": {
            "node_type": "Column",
        }
    }

    node = Node.objects.create(
        namespace="temp", name="a", data_source="test", workspace=create_workspace, metadata=metadata
    )
    table = Node.objects.create(namespace="temp", name="b", data_source="test", workspace=create_workspace)
    Edge.objects.create(
        source=table, destination=node, workspace=create_workspace, metadata={"grai": {"edge_type": "TableToColumn"}}
    )

    assert node.id == uuid.UUID(str(node.id))
    assert node.name == "a"
    assert node.namespace == "temp"
    assert node.data_source == "test"
    assert node.display_name == "a"
    assert node.is_active
    assert isinstance(node.created_at, datetime.datetime)
    assert isinstance(node.updated_at, datetime.datetime)
    assert node.search_type() == "Column"
    assert str(node.table_id()) == str(table.id)


@pytest.mark.django_db
def test_node_created_from_load(create_workspace):
    set_current_tenant(None)
    node = Node.objects.create(namespace="temp2", name="abc", data_source="test", workspace=create_workspace)
    nodes = list(Node.objects.filter(namespace="temp2", name="abc").all())
    assert len(nodes) == 1
    node2 = nodes[0]
    attrs = ["id", "name", "namespace", "data_source", "display_name"]
    for attr in attrs:
        assert getattr(node, attr) == getattr(node2, attr)


@pytest.mark.django_db
def test_edge_created(create_workspace):
    set_current_tenant(None)
    node_a = Node.objects.create(
        namespace="default",
        name="node_a",
        data_source="node_source",
        workspace=create_workspace,
    )
    node_b = Node.objects.create(
        namespace="default",
        name="node_b",
        data_source="node_source",
        workspace=create_workspace,
    )
    edge = Edge.objects.create(
        data_source="edge_source",
        source_id=node_a.id,
        destination_id=node_b.id,
        workspace=create_workspace,
    )

    assert edge.id == uuid.UUID(str(edge.id))
    assert edge.data_source == "edge_source"
    assert edge.is_active
    assert isinstance(edge.metadata, dict) and len(edge.metadata.keys()) == 0
    assert isinstance(edge.created_at, datetime.datetime)
    assert isinstance(edge.updated_at, datetime.datetime)

    assert edge.source == node_a
    assert edge.destination == node_b
