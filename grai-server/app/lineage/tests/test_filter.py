import uuid

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from lineage.filter import apply_table_filter
from lineage.models import Filter, Node
from workspaces.models import Organisation, Workspace


@pytest.fixture
async def test_organisation():
    organisation, created = await Organisation.objects.aget_or_create(name="Test Organisation")

    return organisation


@pytest.fixture
async def test_user():
    User = get_user_model()

    user = User()
    user.set_password("password")
    await sync_to_async(user.save)()

    return user


@pytest.fixture
async def test_workspace(test_organisation):
    workspace = await Workspace.objects.acreate(name=str(uuid.uuid4()), organisation=test_organisation)

    return workspace


@pytest.fixture
def test_filter(test_workspace, test_user):
    return Filter.objects.create(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata={},
        created_by=test_user,
    )


@pytest.mark.django_db
async def test_none(test_filter, test_workspace):
    table = await Node.objects.acreate(
        workspace=test_workspace, metadata={"grai": {"node_type": "Table"}}, name=str(uuid.uuid4())
    )

    queryset = Node.objects.filter(workspace=test_workspace)

    queryset = await apply_table_filter(queryset, test_filter)
    result = await sync_to_async(list)(queryset)
    assert len(result) == 1
    assert str(result[0].id) == str(table.id)


@pytest.mark.django_db
async def test_table_tags_contains(test_workspace, test_user):
    table = await Node.objects.acreate(
        workspace=test_workspace,
        metadata={"grai": {"node_type": "Table", "tags": ["grai-source-postgres"]}},
        name=str(uuid.uuid4()),
    )

    filter = await Filter.objects.acreate(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "table", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects.filter(workspace=test_workspace)

    queryset = await apply_table_filter(queryset, filter)
    result = await sync_to_async(list)(queryset)
    assert len(result) == 1
    assert str(result[0].id) == str(table.id)


@pytest.mark.django_db
async def test_table_tags_contains_miss(test_workspace, test_user):
    await Node.objects.acreate(
        workspace=test_workspace, metadata={"grai": {"node_type": "Table", "tags": []}}, name=str(uuid.uuid4())
    )

    filter = await Filter.objects.acreate(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "table", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects.filter(workspace=test_workspace)

    queryset = await apply_table_filter(queryset, filter)
    result = await sync_to_async(list)(queryset)
    assert result is not None
    assert len(result) == 0


@pytest.mark.django_db
async def test_ancestor_tags_contains(test_workspace, test_user):
    await Node.objects.acreate(
        workspace=test_workspace, metadata={"grai": {"node_type": "Table", "tags": []}}, name=str(uuid.uuid4())
    )

    filter = await Filter.objects.acreate(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "ancestor", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects.filter(workspace=test_workspace)

    await apply_table_filter(queryset, filter)


@pytest.mark.django_db
async def test_no_ancestor_tags_contains(test_workspace, test_user):
    await Node.objects.acreate(
        workspace=test_workspace, metadata={"grai": {"node_type": "Table", "tags": []}}, name=str(uuid.uuid4())
    )

    filter = await Filter.objects.acreate(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "no-ancestor", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects.filter(workspace=test_workspace)

    await apply_table_filter(queryset, filter)


@pytest.mark.django_db
async def test_descendant_tags_contains(test_workspace, test_user):
    await Node.objects.acreate(
        workspace=test_workspace, metadata={"grai": {"node_type": "Table", "tags": []}}, name=str(uuid.uuid4())
    )

    filter = await Filter.objects.acreate(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "descendant", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects.filter(workspace=test_workspace)

    await apply_table_filter(queryset, filter)


@pytest.mark.django_db
async def test_no_descendant_tags_contains(test_workspace, test_user):
    await Node.objects.acreate(
        workspace=test_workspace, metadata={"grai": {"node_type": "Table", "tags": []}}, name=str(uuid.uuid4())
    )

    filter = await Filter.objects.acreate(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "no-descendant", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects.filter(workspace=test_workspace)

    await apply_table_filter(queryset, filter)


@pytest.mark.django_db
async def test_unsupported_type(test_workspace, test_user):
    table = await Node.objects.acreate(
        workspace=test_workspace,
        metadata={"grai": {"node_type": "Table", "tags": ["grai-source-postgres"]}},
        name=str(uuid.uuid4()),
    )

    filter = await Filter.objects.acreate(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "random", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects.filter(workspace=test_workspace)

    with pytest.raises(Exception) as e_info:
        await apply_table_filter(queryset, filter)

    assert str(e_info.value) == "Unknown filter type: random"
