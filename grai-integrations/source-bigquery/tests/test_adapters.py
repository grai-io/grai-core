import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1
from grai_schemas.v1.metadata.edges import ColumnToColumnMetadata, TableToColumnMetadata
from grai_schemas.v1.metadata.nodes import ColumnMetadata, TableMetadata

from grai_source_bigquery.adapters import (
    adapt_to_client,
    build_app_metadata,
    build_grai_metadata,
)
from grai_source_bigquery.models import Column, ColumnID, Edge, Table, TableID
from grai_source_bigquery.package_definitions import config

columns = [
    Column(
        name="test",
        namespace="tests",
        table="test",
        column_schema="test",
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
        table_type="BASE TABLE",
        table_dataset="a_db",
        metadata={"thing": "here"},
    )
]
table_values = [(item, "v1", NodeV1) for item in tables]


@pytest.mark.parametrize("item,version,target", table_values)
def test_table_adapter(item, version, target):
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


source = ColumnID(table_schema="schema", table_name="table", name="id", namespace="test")
destination = ColumnID(table_schema="schema", table_name="table", name="id2", namespace="test")
edges = [Edge(source=source, destination=destination, definition="thing", constraint_type="f")]
edge_values = [(item, "v1", EdgeV1) for item in edges]


def test_column_vs_edge_id():
    from typing import Union

    from pydantic import BaseModel

    class Temp(BaseModel):
        item: Union[ColumnID, TableID]

    data = {"table_name": "test", "table_schema": "test2", "name": "test3", "namespace": "test3"}
    result = Temp(item=data)
    assert isinstance(result.item, ColumnID)


@pytest.mark.xfail
def test_tableid_is_column_id():
    data = {"table_name": "test", "table_schema": "test2", "name": "test3", "namespace": "test3"}
    TableID(**data)


@pytest.mark.parametrize("item,version,target", edge_values)
def test_edge_adapter(item, version, target):
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


def test_make_table_grai_metadata():
    metadata = build_grai_metadata(tables[0], "v1")
    assert isinstance(metadata, GraiNodeMetadataV1)


def test_make_column_grai_metadata():
    metadata = build_grai_metadata(columns[0], "v1")
    assert isinstance(metadata, GraiNodeMetadataV1)


def test_make_edge_grai_metadata():
    metadata = build_grai_metadata(edges[0], "v1")
    assert isinstance(metadata, GraiEdgeMetadataV1)


def test_make_table_bigquery_metadata():
    metadata = build_grai_metadata(tables[0], "v1")
    assert isinstance(metadata, TableMetadata)


def test_make_column_bigquery_metadata():
    metadata = build_grai_metadata(columns[0], "v1")
    assert isinstance(metadata, ColumnMetadata)


def test_make_edge_bigquery_metadata():
    metadata = build_grai_metadata(edges[0], "v1")
    assert isinstance(metadata, ColumnToColumnMetadata)


def test_metadata_has_core_metadata_ids(mock_get_nodes_and_edges):
    nodes, edges = mock_get_nodes_and_edges
    for node in nodes:
        assert hasattr(node.spec.metadata, core_config.metadata_id)

    for edge in edges:
        assert hasattr(edge.spec.metadata, core_config.metadata_id)


def test_metadata_has_bigquery_metadata_id(mock_get_nodes_and_edges):
    nodes, edges = mock_get_nodes_and_edges
    for node in nodes:
        assert hasattr(node.spec.metadata, config.metadata_id)

    for edge in edges:
        assert hasattr(edge.spec.metadata, config.metadata_id)


def test_metadata_is_core_compliant(mock_get_nodes_and_edges):
    nodes, edges = mock_get_nodes_and_edges

    for node in nodes:
        assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), GraiNodeMetadataV1), node.spec.metadata

    for edge in edges:
        assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), GraiEdgeMetadataV1)
