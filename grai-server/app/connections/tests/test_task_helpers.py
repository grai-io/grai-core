import uuid

import pytest
from grai_schemas.v1 import EdgeV1, NodeV1, mock, SourcedNodeV1, SourcedEdgeV1

from connections.task_helpers import get_node, process_updates, update
from lineage.models import Edge, Node, Source
from workspaces.models import Organisation, Workspace


mocker = mock.MockV1()


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


@pytest.fixture
def test_node_v1():
    return SourcedNodeV1.from_spec(
        {
            "name": "node1",
            "namespace": "default",
            "display_name": "node1",
            "metadata": {"grai": {"node_type": "Generic"}},
            "data_source": {"name": "temp"},
        }
    )


@pytest.fixture
def test_edge_v1(test_workspace, test_source_node, test_destination_node):
    return SourcedEdgeV1.from_spec(
        {
            "name": "edge1",
            "namespace": "default",
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
            "data_source": {"name": "temp"},
            "metadata": {"grai": {"edge_type": "Generic"}},
        }
    )


@pytest.fixture
def test_source(test_workspace):
    return Source.objects.create(workspace=test_workspace, name=str(uuid.uuid4()))


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


def mock_node(test_workspace, namespace="default"):
    return Node(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        namespace=namespace,
        metadata={"grai": {"node_type": "Generic"}},
    )


def mock_node_schema(node, test_source, metadata={}):
    spec = {
        "id": node.id,
        "name": node.name,
        "namespace": node.namespace,
        "display_name": node.display_name,
        "workspace": node.workspace.id,
        "metadata": node.metadata,
        "data_source": {"name": test_source.name},
    }
    spec["metadata"].update(metadata)
    return SourcedNodeV1.from_spec(spec)


def mock_edge(source, destination, test_workspace):
    return Edge(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        source=source,
        destination=destination,
        metadata={"grai": {"edge_type": "Generic"}},
    )


def mock_edge_schema(edge, test_source):
    return SourcedEdgeV1.from_spec(
        {
            "id": edge.id,
            "name": edge.name,
            "namespace": edge.namespace,
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
            "data_source": {"name": test_source.name},
        }
    )


class TestUpdate:
    @pytest.mark.django_db
    def test_nodes(self, test_workspace, test_node_v1, test_node, test_source):
        items = [test_node_v1]

        update(test_workspace, test_source, items)

    @pytest.mark.django_db
    def test_create_edges(self, test_workspace, test_source):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        for node in nodes:
            node.save()
        edge = mock_edge(*nodes, test_workspace)
        items = [mock_edge_schema(edge, test_source)]

        update(test_workspace, test_source, items)

    @pytest.mark.django_db
    def test_update_edges(self, test_workspace, test_source):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        for node in nodes:
            node.save()
        edge = mock_edge(*nodes, test_workspace)
        updated_edge = mock_edge_schema(edge, test_source)
        updated_edge.spec.name = "a_new_place"
        items = [updated_edge]

        update(test_workspace, test_source, items)
        db_edge = Edge.objects.filter(name="a_new_place").filter(namespace=edge.namespace).first()
        assert db_edge.name == "a_new_place"

    @pytest.mark.django_db
    def test_empty(self, test_workspace, test_source):
        new, old, updated = process_updates(test_workspace)

    @pytest.mark.django_db
    def test_correct_new_items(self, test_workspace, test_source):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        nodes[0].save()
        mock_nodes = [mock_node_schema(node, test_source) for node in nodes]
        new, old, updated = process_updates(test_workspace, mock_nodes)
        assert len(new) == 1
        assert new[0].name == nodes[1].name

    @pytest.mark.django_db
    def test_correct_updated_items(self, test_workspace, test_source):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        nodes[0].save()
        mock_nodes = [mock_node_schema(node, test_source) for node in nodes]
        new, old, updated = process_updates(test_workspace, mock_nodes)
        assert len(updated) == 1
        assert updated[0].name == nodes[0].name

    @pytest.mark.django_db
    def test_correct_updated_metadata(self, test_workspace, test_source):
        mocker.node.named_node_spec(workspace=test_workspace.id, source=test_source.id)
        nodes = [mock_node(test_workspace) for _ in range(2)]
        nodes[0].metadata["test"] = {"key": "this is a test"}
        nodes[0].save()
        mock_nodes = [mock_node_schema(node, test_source, {"test2": 2}) for node in nodes]
        new, old, updated = process_updates(test_workspace, mock_nodes)
        updated = updated[0].metadata
        assert "test" in updated
        assert isinstance(updated["test"], dict)
        assert updated["test"]["key"] == "this is a test"
        assert "grai" in updated
        assert isinstance(updated["grai"], dict)
        assert updated["grai"]["node_type"] == "Generic"

        assert "test2" in updated["sources"][test_source.name]
        assert updated["sources"][test_source.name]["test2"] == 2

    @pytest.mark.django_db
    def test_process_updates_sourced_node_existing(self, test_workspace, test_source):
        nodes = [mock_node(test_workspace) for _ in range(4)]

        for node in nodes:
            node.save()

        workspace = mocker.workspace.workspace_spec(id=test_workspace.id, name=test_workspace.name)
        source = mocker.source.source_spec(name=test_source.name, id=test_source.id, workspace=workspace.id)
        kwargs = {"data_source": source, "workspace": workspace.id, "namespace": nodes[0].namespace}

        existing_node_spec = [
            mocker.node.named_source_node_spec(name=node.name, id=node.id, **kwargs) for node in nodes
        ]
        new_node_spec = [mocker.node.named_source_node_spec(**kwargs) for node in range(2)]

        created_nodes = [mocker.node.sourced_node(spec=spec) for spec in existing_node_spec]
        updated_nodes = created_nodes[0:2]
        deleted_nodes = created_nodes[2:4]
        new_nodes = [mocker.node.sourced_node(spec=spec) for spec in new_node_spec]

        existing_nodes = []
        for node in created_nodes:
            item = node.spec.dict(exclude_none=True, exclude={"data_source", "workspace"})
            item["data_sources"] = []
            existing_nodes.append(NodeV1.from_spec(item))

        new, deleted, updated = process_updates(test_workspace, [*new_nodes, *updated_nodes], existing_nodes)

        assert len(new) == len(new_nodes)
        new_ids = {(item.name, item.namespace) for item in new}
        new_node_ids = {(item.spec.name, item.spec.namespace) for item in new_nodes}
        assert new_ids == new_node_ids

        assert len(deleted) == len(deleted_nodes)
        deleted_ids = {(item.name, item.namespace) for item in deleted}
        deleted_node_ids = {(item.spec.name, item.spec.namespace) for item in deleted_nodes}
        assert deleted_ids == deleted_node_ids

        assert len(updated) == len(updated_nodes)
        assert all(updated_node.metadata.keys() == {"grai", "sources"} for updated_node in updated)
        assert all(len(updated_node.metadata["sources"]) == 1 for updated_node in updated)
        assert all(test_source.name in updated_node.metadata["sources"] for updated_node in updated)

    @pytest.mark.django_db
    def test_process_updates_sourced_node_default_existing(self, test_workspace, test_source):
        nodes = [mock_node(test_workspace) for _ in range(4)]

        for node in nodes:
            node.save()
        workspace = mocker.workspace.workspace_spec(id=test_workspace.id, name=test_workspace.name)
        source = mocker.source.source_spec(name=test_source.name, id=test_source.id, workspace=workspace.id)

        kwargs = {"data_source": source, "workspace": workspace.id, "namespace": nodes[0].namespace}

        existing_node_spec = [mocker.node.named_source_node_spec(name=node.name, **kwargs) for node in nodes]
        new_node_spec = [mocker.node.named_source_node_spec(**kwargs) for node in range(2)]

        created_nodes = [mocker.node.sourced_node(spec=spec) for spec in existing_node_spec]

        updated_nodes = created_nodes[0:2]
        deleted_nodes = created_nodes[2:4]
        new_nodes = [mocker.node.sourced_node(spec=spec) for spec in new_node_spec]

        new, deleted, updated = process_updates(test_workspace, [*new_nodes, *updated_nodes])

        assert len(new) == len(new_nodes)
        new_ids = {(item.name, item.namespace) for item in new}
        new_node_ids = {(item.spec.name, item.spec.namespace) for item in new_nodes}
        assert new_ids == new_node_ids

        assert len(deleted) == len(deleted_nodes)
        deleted_ids = {(item.name, item.namespace) for item in deleted}
        deleted_node_ids = {(item.spec.name, item.spec.namespace) for item in deleted_nodes}
        assert deleted_ids == deleted_node_ids

        assert len(updated) == len(updated_nodes)
        assert all(updated_node.metadata.keys() == {"grai", "sources"} for updated_node in updated)
        assert all(len(updated_node.metadata["sources"]) == 1 for updated_node in updated)
        assert all(test_source.name in updated_node.metadata["sources"] for updated_node in updated)

    @pytest.mark.django_db
    def test_process_updates_sourced_edge_existing(self, test_workspace, test_source):
        edges = [mock_edge(*[mock_node(test_workspace) for _ in range(2)], test_workspace) for _ in range(4)]
        for edge in edges:
            edge.source.save()
            edge.destination.save()
            edge.save()

        source = mocker.source.source_spec(name=test_source.name, id=test_source.id, workspace=test_workspace.id)
        workspace = mocker.workspace.workspace_spec(id=test_workspace.id, name=test_workspace.name)
        kwargs = {"data_source": source, "workspace": workspace.id, "namespace": edges[0].namespace}

        existing_edge_spec = []
        for edge in edges:
            source = {"name": edge.source.name, "namespace": edge.source.namespace, "id": str(edge.source.id)}
            destination = {
                "name": edge.destination.name,
                "namespace": edge.destination.namespace,
                "id": str(edge.destination.id),
            }
            mock_spec = mocker.edge.named_source_edge_spec(
                name=edge.name, source=source, destination=destination, id=edge.id, **kwargs
            )
            existing_edge_spec.append(mock_spec)

        edge_nodes = [mock_node(test_workspace) for _ in range(3)]

        for node in edge_nodes:
            node.save()
        new_edge_spec = []
        for i, edge in enumerate(range(2)):
            source = {
                "name": edge_nodes[0 + i].name,
                "namespace": edge_nodes[0 + i].namespace,
                "id": str(edge_nodes[0 + i].id),
            }
            destination = {
                "name": edge_nodes[1 + i].name,
                "namespace": edge_nodes[1 + i].namespace,
                "id": str(edge_nodes[1 + i].id),
            }
            mock_spec = mocker.edge.named_source_edge_spec(**kwargs, source=source, destination=destination)
            new_edge_spec.append(mock_spec)

        created_edges = [mocker.edge.sourced_edge(spec=spec) for spec in existing_edge_spec]
        updated_edges = created_edges[0:2]
        deleted_edges = created_edges[2:4]
        new_edges = [mocker.edge.sourced_edge(spec=spec) for spec in new_edge_spec]

        existing_edges = []
        for edge in created_edges:
            item = edge.spec.dict(exclude_none=True, exclude={"data_source", "workspace"})
            item["data_sources"] = []
            existing_edges.append(EdgeV1.from_spec(item))

        new, deleted, updated = process_updates(test_workspace, [*new_edges, *updated_edges], existing_edges)

        assert len(new) == len(new_edges)
        new_ids = {(item.name, item.namespace) for item in new}
        new_edge_ids = {(item.spec.name, item.spec.namespace) for item in new_edges}
        assert new_ids == new_edge_ids

        assert len(deleted) == len(deleted_edges)
        deleted_ids = {(item.name, item.namespace) for item in deleted}
        deleted_edge_ids = {(item.spec.name, item.spec.namespace) for item in deleted_edges}
        assert deleted_ids == deleted_edge_ids

        assert len(updated) == len(updated_edges)
        assert all(updated_edge.metadata.keys() == {"grai", "sources"} for updated_edge in updated)
        assert all(len(updated_edge.metadata["sources"]) == 1 for updated_edge in updated)
        assert all(test_source.name in updated_edge.metadata["sources"] for updated_edge in updated)

    @pytest.mark.django_db
    def test_process_updates_sourced_edge_default_existing(self, test_workspace, test_source):
        edges = [mock_edge(*[mock_node(test_workspace) for _ in range(2)], test_workspace) for _ in range(4)]
        for edge in edges:
            edge.source.save()
            edge.destination.save()
            edge.save()

        workspace = mocker.workspace.workspace_spec(id=test_workspace.id, name=test_workspace.name)
        source = mocker.source.source_spec(name=test_source.name, id=test_source.id, workspace=workspace.id)

        kwargs = {"data_source": source, "workspace": workspace.id, "namespace": edges[0].namespace}

        existing_edge_spec = []
        for edge in edges:
            source = {"name": edge.source.name, "namespace": edge.source.namespace, "id": str(edge.source.id)}
            destination = {
                "name": edge.destination.name,
                "namespace": edge.destination.namespace,
                "id": str(edge.destination.id),
            }
            mock_spec = mocker.edge.named_source_edge_spec(
                name=edge.name, source=source, destination=destination, **kwargs
            )
            existing_edge_spec.append(mock_spec)

        edge_nodes = [mock_node(test_workspace) for _ in range(3)]
        for node in edge_nodes:
            node.save()

        new_edge_spec = []
        for i, edge in enumerate(range(2)):
            source = {
                "name": edge_nodes[0 + i].name,
                "namespace": edge_nodes[0 + i].namespace,
                "id": str(edge_nodes[0 + i].id),
            }
            destination = {
                "name": edge_nodes[1 + i].name,
                "namespace": edge_nodes[1 + i].namespace,
                "id": str(edge_nodes[1 + i].id),
            }
            mock_spec = mocker.edge.named_source_edge_spec(**kwargs, source=source, destination=destination)
            new_edge_spec.append(mock_spec)

        created_edges = [mocker.edge.sourced_edge(spec=spec) for spec in existing_edge_spec]
        updated_edges = created_edges[0:2]
        deleted_edges = created_edges[2:4]
        new_edges = [mocker.edge.sourced_edge(spec=spec) for spec in new_edge_spec]

        new, deleted, updated = process_updates(test_workspace, [*new_edges, *updated_edges])

        assert len(new) == len(new_edges)
        new_ids = {(item.name, item.namespace) for item in new}
        new_edge_ids = {(item.spec.name, item.spec.namespace) for item in new_edges}
        assert new_ids == new_edge_ids

        assert len(deleted) == len(deleted_edges)
        deleted_ids = {(item.name, item.namespace) for item in deleted}
        deleted_edge_ids = {(item.spec.name, item.spec.namespace) for item in deleted_edges}
        assert deleted_ids == deleted_edge_ids

        assert len(updated) == len(updated_edges)
        assert all(updated_edge.metadata.keys() == {"grai", "sources"} for updated_edge in updated)
        assert all(len(updated_edge.metadata["sources"]) == 1 for updated_edge in updated)
        assert all(test_source.name in updated_edge.metadata["sources"] for updated_edge in updated)

    @pytest.mark.django_db
    def test_deactivated(self, test_workspace, test_source):
        nodes = [mock_node(test_workspace) for _ in range(2)]
        for node in nodes:
            node.save()
        mock_nodes = [mock_node_schema(node, test_source) for node in nodes]
        existing_nodes = []
        for node in mock_nodes:
            item = node.spec.dict(exclude_none=True, exclude={"data_source", "workspace"})
            item["data_sources"] = []
            existing_nodes.append(NodeV1.from_spec(item))

        update(test_workspace, test_source, mock_nodes[:1], existing_nodes)
