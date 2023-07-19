from typing import Union

import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1
from grai_schemas.v1.metadata.edges import ColumnToColumnMetadata, TableToColumnMetadata
from grai_schemas.v1.metadata.nodes import ColumnMetadata, TableMetadata
from grai_schemas.v1.source import SourceV1
from pydantic import BaseModel

from grai_source_bigquery.adapters import (
    adapt_to_client,
    build_app_metadata,
    build_grai_metadata,
)
from grai_source_bigquery.models import Column, ColumnID, Edge, Table, TableID
from grai_source_bigquery.package_definitions import config


@pytest.fixture
def mock_column():
    return Column(
        name="test",
        namespace="tests",
        table="test",
        column_schema="test",
        data_type="integer",
        is_nullable=True,
        default_value="Orange",
        is_pk=True,
    )


@pytest.fixture
def mock_table():
    return Table(
        name="test",
        namespace="tests",
        table_schema="test",
        columns=[],
        table_type="BASE TABLE",
        table_dataset="a_db",
        metadata={"thing": "here"},
    )


@pytest.fixture
def mock_edge():
    source = ColumnID(table_schema="schema", table_name="table", name="id", namespace="test")
    destination = ColumnID(table_schema="schema", table_name="table", name="id2", namespace="test")
    return Edge(source=source, destination=destination, definition="thing", constraint_type="f")


def test_column_adapter(mock_source, mock_column):
    adapted = adapt_to_client(mock_column, mock_source, "v1")
    assert isinstance(adapted, SourcedNodeV1)


def test_table_adapter(mock_source, mock_table):
    adapted = adapt_to_client(mock_table, mock_source, "v1")
    assert isinstance(adapted, SourcedNodeV1)


def test_column_vs_edge_id():
    class Temp(BaseModel):
        item: Union[ColumnID, TableID]

    data = {"table_name": "test", "table_schema": "test2", "name": "test3", "namespace": "test3"}
    result = Temp(item=data)
    assert isinstance(result.item, ColumnID)


@pytest.mark.xfail
def test_tableid_is_column_id():
    """ """
    data = {"table_name": "test", "table_schema": "test2", "name": "test3", "namespace": "test3"}
    TableID(**data)


def test_edge_adapter(mock_source, mock_edge):
    result = adapt_to_client(mock_edge, mock_source, "v1")
    assert isinstance(result, SourcedEdgeV1)


def test_make_table_grai_metadata(mock_table):
    """ """
    metadata = build_grai_metadata(mock_table, "v1")
    assert isinstance(metadata, GraiNodeMetadataV1)


def test_make_column_grai_metadata(mock_column):
    """ """
    metadata = build_grai_metadata(mock_column, "v1")
    assert isinstance(metadata, GraiNodeMetadataV1)


def test_make_edge_grai_metadata(mock_edge):
    """ """
    metadata = build_grai_metadata(mock_edge, "v1")
    assert isinstance(metadata, GraiEdgeMetadataV1)


def test_make_table_bigquery_metadata(mock_table):
    """ """
    metadata = build_grai_metadata(mock_table, "v1")
    assert isinstance(metadata, TableMetadata)


def test_make_column_bigquery_metadata(mock_column):
    """ """
    metadata = build_grai_metadata(mock_column, "v1")
    assert isinstance(metadata, ColumnMetadata)


def test_make_edge_bigquery_metadata(mock_edge):
    """ """
    metadata = build_grai_metadata(mock_edge, "v1")
    assert isinstance(metadata, ColumnToColumnMetadata)


# def test_metadata_has_core_metadata_ids(mock_get_nodes_and_edges):
#     """
#
#     Args:
#         mock_get_nodes_and_edges:
#
#     Returns:
#
#     Raises:
#
#     """
#     nodes, edges = mock_get_nodes_and_edges
#     for node in nodes:
#         assert hasattr(node.spec.metadata, core_config.metadata_id)
#
#     for edge in edges:
#         assert hasattr(edge.spec.metadata, core_config.metadata_id)
#
#
# def test_metadata_has_bigquery_metadata_id(mock_get_nodes_and_edges):
#     """
#
#     Args:
#         mock_get_nodes_and_edges:
#
#     Returns:
#
#     Raises:
#
#     """
#     nodes, edges = mock_get_nodes_and_edges
#     for node in nodes:
#         assert hasattr(node.spec.metadata, config.metadata_id)
#
#     for edge in edges:
#         assert hasattr(edge.spec.metadata, config.metadata_id)
#
#
# def test_metadata_is_core_compliant(mock_get_nodes_and_edges):
#     """
#
#     Args:
#         mock_get_nodes_and_edges:
#
#     Returns:
#
#     Raises:
#
#     """
#     nodes, edges = mock_get_nodes_and_edges
#
#     for node in nodes:
#         assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), GraiNodeMetadataV1), node.spec.metadata
#
#     for edge in edges:
#         assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), GraiEdgeMetadataV1)
