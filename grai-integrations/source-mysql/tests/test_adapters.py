import pytest
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1
from grai_schemas import config as core_config
from grai_schemas.models import GraiEdgeMetadata, GraiNodeMetadata

from grai_source_mysql.adapters import adapt_to_client
from grai_source_mysql.models import Column, ColumnID, Edge, Table
from grai_source_mysql.package_definitions import config

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


def test_metadata_has_core_metadata_ids(nodes_and_edges):
    nodes, edges = nodes_and_edges
    for node in nodes:
        assert core_config.metadata_id in node.spec.metadata

    for edge in edges:
        assert core_config.metadata_id in edge.spec.metadata


def test_metadata_has_dbt_metadata_id(nodes_and_edges):
    nodes, edges = nodes_and_edges
    for node in nodes:
        assert config.metadata_id in node.spec.metadata

    for edge in edges:
        assert config.metadata_id in edge.spec.metadata


def test_metadata_is_core_compliant(nodes_and_edges):
    nodes, edges = nodes_and_edges

    for node in nodes:
        assert isinstance(node.spec.metadata[core_config.metadata_id], GraiNodeMetadata)

    for edge in edges:
        assert isinstance(edge.spec.metadata[core_config.metadata_id], GraiEdgeMetadata)
