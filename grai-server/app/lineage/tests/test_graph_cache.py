import uuid

import pytest

from lineage.graph_cache import GraphCache
from lineage.models import Edge, Node
from workspaces.admin import ExtendedGraphCache
from workspaces.models import Organisation, Workspace


@pytest.fixture
def create_organisation(name: str = None):
    return Organisation.objects.create(name=str(uuid.uuid4()) if name is None else name)


@pytest.fixture
def create_workspace(create_organisation, name: str = None):
    return Workspace.objects.create(
        name=str(uuid.uuid4()) if name is None else name,
        organisation=create_organisation,
    )


@pytest.mark.django_db
def test_build_cache(create_workspace):
    client = ExtendedGraphCache(workspace=create_workspace)

    node = Node.objects.create(
        workspace=create_workspace,
        name=str(uuid.uuid4()),
    )
    destination = Node.objects.create(
        workspace=create_workspace,
        name=str(uuid.uuid4()),
    )
    Edge.objects.create(workspace=create_workspace, source=node, destination=destination)

    client.build_cache()


@pytest.mark.django_db
def test_clear_cache(create_workspace):
    client = ExtendedGraphCache(workspace=create_workspace)

    client.clear_cache()


@pytest.mark.django_db
def test_update_node(create_workspace):
    client = GraphCache(workspace=create_workspace)

    client.update_node(id="1", x=1, y=1)


@pytest.mark.django_db
def test_layout(create_workspace):
    source = Node.objects.create(
        workspace=create_workspace,
        name=str(uuid.uuid4()),
        metadata={"grai": {"node_type": "Table"}},
    )
    destination = Node.objects.create(
        workspace=create_workspace,
        name=str(uuid.uuid4()),
        metadata={"grai": {"node_type": "Table"}},
    )

    [
        Node.objects.create(
            workspace=create_workspace,
            name=str(uuid.uuid4()),
            metadata={"grai": {"node_type": "Table"}},
        )
        for i in range(25)
    ]

    Edge.objects.create(
        workspace=create_workspace,
        source=source,
        destination=destination,
        metadata={
            "grai": {
                "edge_type": "TableToTable",
            }
        },
    )

    client = ExtendedGraphCache(workspace=create_workspace)

    client.build_cache()

    client.layout_graph()
