import uuid

import pytest
from lineage.graph_cache import GraphCache
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
async def test_clear_cache(create_workspace):
    client = GraphCache(workspace=create_workspace)

    client.clear_cache()
