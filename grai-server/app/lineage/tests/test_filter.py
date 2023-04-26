from api.tests.common import test_organisation, test_user, test_workspace
import pytest
from lineage.filter import apply_table_filter
from lineage.models import Node, Filter

import uuid


@pytest.fixture
def test_filter(test_workspace, test_user):
    return Filter.objects.create(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata={},
        created_by=test_user,
    )


@pytest.mark.django_db
def test_none(test_filter, test_workspace):
    table = Node.objects.create(workspace=test_workspace, metadata={"grai": {"node_type": "Table"}}, name=uuid.uuid4())

    queryset = Node.objects

    result = apply_table_filter(queryset, test_filter)
    assert result is not None
    assert len(result) == 1
    assert str(result[0].id) == str(table.id)


@pytest.mark.django_db
def test_table_tags_contains(test_workspace, test_user):
    table = Node.objects.create(
        workspace=test_workspace,
        metadata={"grai": {"node_type": "Table", "tags": ["grai-source-postgres"]}},
        name=uuid.uuid4(),
    )

    filter = Filter.objects.create(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "table", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects

    result = apply_table_filter(queryset, filter)
    assert result is not None
    assert len(result) == 1
    assert str(result[0].id) == str(table.id)


@pytest.mark.django_db
def test_table_tags_contains_miss(test_workspace, test_user):
    table = Node.objects.create(
        workspace=test_workspace, metadata={"grai": {"node_type": "Table", "tags": []}}, name=uuid.uuid4()
    )

    filter = Filter.objects.create(
        workspace=test_workspace,
        name=str(uuid.uuid4()),
        metadata=[{"field": "tag", "operator": "contains", "type": "table", "value": "grai-source-postgres"}],
        created_by=test_user,
    )

    queryset = Node.objects

    result = apply_table_filter(queryset, filter)
    assert result is not None
    assert len(result) == 0
