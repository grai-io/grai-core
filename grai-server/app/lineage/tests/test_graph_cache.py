import uuid

import pytest

from lineage.graph_cache import GraphCache
from workspaces.models import Organisation, Workspace
from lineage.models import Node, Edge


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
    client = GraphCache(workspace=create_workspace)

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
    client = GraphCache(workspace=create_workspace)

    client.clear_cache()
