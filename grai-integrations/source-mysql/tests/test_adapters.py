import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1
from grai_schemas.v1.metadata.edges import ColumnToColumnMetadata, TableToColumnMetadata
from grai_schemas.v1.metadata.nodes import ColumnMetadata, TableMetadata

from grai_source_mysql.adapters import adapt_to_client, build_grai_metadata
from grai_source_mysql.models import Column, ColumnID, Edge, Table, TableID
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
        column_key="PRI",
    )
]
column_values = [(item, "v1", NodeV1) for item in columns]


@pytest.mark.parametrize("item,version,target", column_values)
def test_column_adapter(item, version, target):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


def test_column_metadata():
    """ """
    col = Column(
        name="test",
        namespace="tests",
        table="test",
        schema="test",
        data_type="integer",
        is_nullable=True,
        default_value="Orange",
        column_key="PRI",
    )
    adapted_col = adapt_to_client(col, "v1")
    node_attributes = adapted_col.spec.metadata.grai.node_attributes
    assert node_attributes.is_unique
    assert node_attributes.is_primary_key
    assert node_attributes.data_type == "integer"
    assert node_attributes.default_value.default_value == "Orange"


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
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


source = ColumnID(table_schema="schema", table_name="table", name="id", namespace="test")
destination = ColumnID(table_schema="schema", table_name="table", name="id2", namespace="test")
edges = [Edge(source=source, destination=destination, definition="thing", constraint_type="f")]
edge_values = [(item, "v1", EdgeV1) for item in edges]


@pytest.mark.xfail
def test_table_id_is_column_id():
    """ """
    data = {"table_name": "test", "table_schema": "test2", "name": "test3", "namespace": "test3"}
    TableID(**data)


def test_make_table_metadata():
    """ """
    metadata = build_grai_metadata(tables[0], "v1")
    assert isinstance(metadata, TableMetadata)


def test_make_column_metadata():
    """ """
    metadata = build_grai_metadata(columns[0], "v1")
    assert isinstance(metadata, ColumnMetadata)


def test_make_edge_metadata():
    """ """
    metadata = build_grai_metadata(edges[0], "v1")
    assert isinstance(metadata, ColumnToColumnMetadata)


@pytest.mark.parametrize("item,version,target", edge_values)
def test_edge_adapter(item, version, target):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


def test_metadata_has_core_metadata_ids(nodes_and_edges):
    """

    Args:
        nodes_and_edges:

    Returns:

    Raises:

    """
    nodes, edges = nodes_and_edges
    for node in nodes:
        assert hasattr(node.spec.metadata, core_config.metadata_id)

    for edge in edges:
        assert hasattr(edge.spec.metadata, core_config.metadata_id)


def test_metadata_has_mysql_metadata_id(nodes_and_edges):
    """

    Args:
        nodes_and_edges:

    Returns:

    Raises:

    """
    nodes, edges = nodes_and_edges
    for node in nodes:
        assert hasattr(node.spec.metadata, config.metadata_id)

    for edge in edges:
        assert hasattr(edge.spec.metadata, config.metadata_id)


def test_metadata_is_core_compliant(nodes_and_edges):
    """

    Args:
        nodes_and_edges:

    Returns:

    Raises:

    """
    nodes, edges = nodes_and_edges

    for node in nodes:
        assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), GraiNodeMetadataV1), node.spec.metadata

    for edge in edges:
        assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), GraiEdgeMetadataV1)
