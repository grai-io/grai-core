import pytest
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1

from grai_source_postgres.adapters import adapt_to_client
from grai_source_postgres.models import Column, ColumnID, Edge, Table

columns = [
    Column(
        name="test",
        namespace="tests",
        table="test",
        schema="test",
        data_type="integer",
        is_nullable=True,
        default_value="Orange",
        is_pk=True,
    )
]
column_values = [(item, "v1", NodeV1) for item in columns]


@pytest.mark.parametrize("item,version,target", column_values)
def test_column_adapter(item, version, target):
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


tables = [
    Table(
        name="test",
        namespace="tests",
        table_schema="test",
        columns=[],
        metadata={"thing": "here"},
    )
]
table_values = [(item, "v1", NodeV1) for item in tables]


@pytest.mark.parametrize("item,version,target", table_values)
def test_table_adapter(item, version, target):
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


source = ColumnID(
    table_schema="schema", table_name="table", name="id", namespace="test"
)
destination = ColumnID(
    table_schema="schema", table_name="table", name="id2", namespace="test"
)
edges = [
    Edge(
        source=source, destination=destination, definition="thing", constraint_type="f"
    )
]
edge_values = [(item, "v1", EdgeV1) for item in edges]


@pytest.mark.parametrize("item,version,target", edge_values)
def test_edge_adapter(item, version, target):
    result = adapt_to_client(item, version)
    assert isinstance(result, target)
