import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1

from grai_source_fivetran.adapters import adapt_to_client
from grai_source_fivetran.models import Column, Edge, Table
from grai_source_fivetran.package_definitions import config


def mock_edge_values():
    extra_args = {
        "is_primary_key": True,
        "is_foreign_key": False,
        "fivetran_id": "abc",
        "fivetran_table_id": "123",
    }
    source = Column(table_schema="schema", table_name="table", name="id", namespace="test", **extra_args)
    destination = Column(table_schema="schema", table_name="table", name="id2", namespace="test", **extra_args)
    test_edge = [
        Edge(
            source=source,
            destination=destination,
            definition="thing",
            constraint_type="c",
        )
    ]
    return test_edge


class AdapterTestValues:
    columns = [
        Column(
            name="test",
            namespace="tests",
            table_name="test",
            table_schema="test",
            is_primary_key=True,
            is_foreign_key=False,
            fivetran_id="easyas",
            fivetran_table_id="abc123",
        )
    ]

    tables = [
        Table(
            name="test",
            namespace="tests",
            schema_name="test",
            fivetran_id="test",
        )
    ]

    edges = mock_edge_values()


@pytest.mark.parametrize("item,version,target", [(item, "v1", NodeV1) for item in AdapterTestValues.columns])
def test_column_adapter(item, version, target):
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


@pytest.mark.parametrize("item,version,target", [(item, "v1", NodeV1) for item in AdapterTestValues.tables])
def test_table_adapter(item, version, target):
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


@pytest.mark.parametrize("item,version,target", [(item, "v1", EdgeV1) for item in AdapterTestValues.edges])
def test_edge_adapter(item, version, target):
    result = adapt_to_client(item, version)
    assert isinstance(result, target)


def test_node_metadata_has_core_metadata_ids(nodes):
    for node in nodes:
        assert hasattr(node.spec.metadata, core_config.metadata_id)


def test_edge_metadata_has_core_metadata_ids(edges):
    for edge in edges:
        assert hasattr(edge.spec.metadata, core_config.metadata_id)


def test_node_metadata_has_app_metadata_id(nodes):
    for node in nodes:
        assert hasattr(node.spec.metadata, config.metadata_id)


def test_edge_metadata_has_app_metadata_id(edges):
    for edge in edges:
        assert hasattr(edge.spec.metadata, config.metadata_id)


def test_node_metadata_is_core_compliant(nodes):
    for node in nodes:
        assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), GraiNodeMetadataV1)


def test_edge_metadata_is_core_compliant(edges):
    for edge in edges:
        assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), GraiEdgeMetadataV1)
