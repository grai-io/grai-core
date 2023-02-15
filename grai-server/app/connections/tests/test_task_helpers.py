import uuid

import pytest
from grai_schemas.v1 import EdgeV1, NodeV1

from connections.task_helpers import get_node, process_updates, update
from lineage.models import Edge, Node
from workspaces.models import Organisation, Workspace


@pytest.fixture
def test_organisation():
    return Organisation.objects.create(name="Org1")


@pytest.fixture
def test_workspace(test_organisation):
    return Workspace.objects.create(name="W1", organisation=test_organisation)


@pytest.fixture
def test_node(test_workspace):
    return Node.objects.create(workspace=test_workspace, name="N1")


@pytest.fixture
def test_source_node(test_workspace):
    return Node.objects.create(workspace=test_workspace, name="S1")


@pytest.fixture
def test_destination_node(test_workspace):
    return Node.objects.create(workspace=test_workspace, name="D1")


@pytest.fixture
def test_edge(test_workspace, test_source_node, test_destination_node):
    return Edge.objects.create(
        workspace=test_workspace,
        name="N1",
        source=test_source_node,
        destination=test_destination_node,
    )


@pytest.fixture
def test_node_v1():
    return NodeV1.from_spec(
        {
            "name": "node1",
            "namespace": "default",
            "data_source": "test",
            "display_name": "node1",
            "metadata": {"grai": {"node_type": "Node"}},
        }
    )


@pytest.fixture
def test_edge_v1(test_workspace, test_source_node, test_destination_node):
    return EdgeV1.from_spec(
        {
            "name": "edge1",
            "namespace": "default",
            "data_source": "test",
            "display_name": "edge1",
            "source": {
                "name": "node1",
                "namespace": "default",
                "id": str(test_source_node.id),
            },
            "destination": {
                "name": "node2",
                "namespace": "default",
                "id": str(test_destination_node.id),
            },
            "metadata": {"grai": {"edge_type": "Edge"}},
        }
    )


class TestGetNode:
    @pytest.mark.django_db
    def test_id(self, test_workspace):
        grai_type = {
            "name": "model1",
            "namespace": "default",
            "id": "85a3c968-15c4-4906-83ff-931a672c087f",
        }

        node = get_node(test_workspace, grai_type)

        assert str(node.id) == "85a3c968-15c4-4906-83ff-931a672c087f"

    @pytest.mark.django_db
    def test_node(self, test_workspace):
        node = Node.objects.create(name="model1", namespace="default", workspace=test_workspace)

        grai_type = {"name": "model1", "namespace": "default"}

        result = get_node(test_workspace, grai_type)

        assert result.id == node.id
        assert result.name == node.name
        assert result.namespace == node.namespace

    @pytest.mark.django_db
    def test_no_node(self, test_workspace):
        grai_type = {"name": "model1", "namespace": "default"}

        with pytest.raises(Exception) as e_info:
            get_node(test_workspace, grai_type)

        assert str(e_info.value) == "Node matching query does not exist."


def mock_node(test_workspace):
    return Node(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        data_source="test",
        metadata={"grai": {"node_type": "Node"}},
    )


def mock_node_schema(node, metadata={}):
    spec = {
        "name": node.name,
        "namespace": node.namespace,
        "data_source": node.data_source,
        "display_name": node.display_name,
        "workspace": node.workspace.id,
        "metadata": node.metadata,
    }
    spec["metadata"].update(metadata)
    return NodeV1.from_spec(spec)


def mock_edge(source, destination, test_workspace):
    return Edge(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        source=source,
        destination=destination,
        metadata={"grai": {"edge_type": "Edge"}},
    )


def mock_edge_schema(edge):
    return EdgeV1.from_spec(
        {
            "name": edge.name,
            "namespace": edge.namespace,
            "data_source": edge.data_source,
            "display_name": edge.display_name,
            "source": {
                "name": edge.source.name,
                "namespace": edge.source.namespace,
                "id": str(edge.source.id),
            },
            "destination": {
                "name": edge.destination.name,
                "namespace": edge.destination.namespace,
                "id": str(edge.destination.id),
            },
            "metadata": edge.metadata,
        }
    )


class TestUpdate:
    @pytest.mark.django_db
    def test_nodes(self, test_workspace, test_node_v1, test_node):
        items = [test_node_v1]

        update(test_workspace, items)

    @pytest.mark.django_db
    def test_create_edges(self, test_workspace):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        for node in nodes:
            node.save()
        edge = mock_edge(*nodes, test_workspace)
        items = [mock_edge_schema(edge)]

        update(test_workspace, items)

    @pytest.mark.django_db
    def test_update_edges(self, test_workspace):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        for node in nodes:
            node.save()
        edge = mock_edge(*nodes, test_workspace)
        updated_edge = mock_edge_schema(edge)
        updated_edge.spec.data_source = "a_new_place"
        items = [updated_edge]

        update(test_workspace, items)
        db_edge = Edge.objects.filter(name=edge.name).filter(namespace=edge.namespace).first()
        assert db_edge.data_source == "a_new_place"

    @pytest.mark.django_db
    def test_correct_new_items(self, test_workspace):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        nodes[0].save()
        mock_nodes = [mock_node_schema(node) for node in nodes]
        new, old, updated = process_updates(test_workspace, Node, mock_nodes)
        assert len(new) == 1
        assert new[0].name == nodes[1].name

    @pytest.mark.django_db
    def test_correct_updated_items(self, test_workspace):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        nodes[0].save()
        mock_nodes = [mock_node_schema(node) for node in nodes]
        new, old, updated = process_updates(test_workspace, Node, mock_nodes)
        assert len(updated) == 1
        assert updated[0].name == nodes[0].name

    @pytest.mark.django_db
    def test_correct_updated_metadata(self, test_workspace):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        nodes[0].metadata["test"] = {"key": "this is a test"}
        nodes[0].save()
        mock_nodes = [mock_node_schema(node, {"test2": 2}) for node in nodes]
        new, old, updated = process_updates(test_workspace, Node, mock_nodes)
        updated = updated[0].metadata
        assert "test" in updated
        assert isinstance(updated["test"], dict)
        assert updated["test"]["key"] == "this is a test"
        assert "grai" in updated
        assert isinstance(updated["grai"], dict)
        assert updated["grai"]["node_type"] == "Node"

        assert "test2" in updated
        assert updated["test2"] == 2
