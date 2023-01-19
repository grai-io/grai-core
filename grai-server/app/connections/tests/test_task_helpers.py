import pytest
from connections.task_helpers import deactivate, get_node, update
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeID, NodeV1
from lineage.models import Edge, Node
from workspaces.models import Workspace, Organisation


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
            "source": NodeID(
                name="node1",
                namespace="default",
                id=str(test_source_node.id),
            ),
            "destination": NodeID(
                name="node2",
                namespace="default",
                id=str(test_destination_node.id),
            ),
        }
    )


class TestGetNode:
    @pytest.mark.django_db
    def test_id(self, test_workspace):
        grai_type = NodeID(
            name="model1",
            namespace="default",
            id="85a3c968-15c4-4906-83ff-931a672c087f",
        )

        node = get_node(test_workspace, grai_type)

        assert str(node.id) == "85a3c968-15c4-4906-83ff-931a672c087f"

    @pytest.mark.django_db
    def test_node(self, test_workspace):
        node = Node.objects.create(
            name="model1", namespace="default", workspace=test_workspace
        )

        grai_type = NodeID(name="model1", namespace="default")

        result = get_node(test_workspace, grai_type)

        assert result.id == node.id
        assert result.name == node.name
        assert result.namespace == node.namespace

    @pytest.mark.django_db
    def test_no_node(self, test_workspace):
        grai_type = NodeID(name="model1", namespace="default")

        with pytest.raises(Exception) as e_info:
            get_node(test_workspace, grai_type)

        assert str(e_info.value) == "Node matching query does not exist."


class TestDeactivate:
    @pytest.mark.django_db
    def test_nodes(self, test_node_v1):
        items = [test_node_v1]

        result = deactivate(items)

        assert len(result) == 1

        assert result[0].spec.name == "node1"
        assert result[0].spec.is_active == False

    @pytest.mark.django_db
    def test_empty_list(self):
        items = []

        result = deactivate(items)

        assert len(result) == 0


class TestUpdate:
    @pytest.mark.django_db
    def test_nodes(self, test_workspace, test_node_v1, test_node):
        items = [test_node_v1]

        update(test_workspace, items)

    @pytest.mark.django_db
    def test_edges(self, test_workspace, test_edge_v1, test_edge):
        items = [test_edge_v1]

        update(test_workspace, items)

    @pytest.mark.django_db
    def test_empty_list(self, test_workspace):
        items = []

        update(test_workspace, items)
