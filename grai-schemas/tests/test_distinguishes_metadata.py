from grai_schemas.base import GraiMetadata
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnAttributes,
    ColumnToColumnMetadata,
    GenericEdgeMetadataV1,
)
from grai_schemas.v1.metadata.edges import Metadata as GraiEdgeMetadata
from grai_schemas.v1.metadata.edges import (
    TableToColumnAttributes,
    TableToColumnMetadata,
)
from grai_schemas.v1.metadata.nodes import (
    ColumnAttributes,
    ColumnMetadata,
    GenericNodeMetadataV1,
)
from grai_schemas.v1.metadata.nodes import Metadata as GraiNodeMetadata
from grai_schemas.v1.metadata.nodes import TableAttributes, TableMetadata


def test_distinguishes_generic_node_metadata():
    spec = {"grai": {"node_type": "Node", "node_attributes": {}}}

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiNodeMetadata)
    assert isinstance(obj.grai, GenericNodeMetadataV1)
    assert isinstance(obj.grai.node_attributes, dict)


def test_distinguishes_column_metadata():
    spec = {"grai": {"node_type": "Column", "node_attributes": {"is_primary_key": True}}}

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiNodeMetadata)
    assert isinstance(obj.grai, GenericNodeMetadataV1)
    assert isinstance(obj.grai, ColumnMetadata)
    assert isinstance(obj.grai.node_attributes, ColumnAttributes)


def test_distinguishes_table_metadata():
    spec = {"grai": {"node_type": "Table", "node_attributes": {"is_primary_key": True}}}

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiNodeMetadata)
    assert isinstance(obj.grai, GenericNodeMetadataV1)
    assert isinstance(obj.grai, TableMetadata)
    assert isinstance(obj.grai.node_attributes, TableAttributes)


def test_distinguishes_generic_edge_metadata():
    spec = {
        "grai": {
            "edge_type": "Edge",
            "edge_attributes": {},
        }
    }

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiEdgeMetadata)
    assert isinstance(obj.grai, GenericEdgeMetadataV1)
    assert isinstance(obj.grai.edge_attributes, dict)


def test_distinguishes_column_to_column_metadata():
    spec = {
        "grai": {
            "edge_type": "ColumnToColumn",
            "edge_attributes": {"preserves_unique": True},
        }
    }

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiEdgeMetadata)
    assert isinstance(obj.grai, GenericEdgeMetadataV1)
    assert isinstance(obj.grai, ColumnToColumnMetadata)
    assert isinstance(obj.grai.edge_attributes, ColumnToColumnAttributes)


def test_metadata_distinguishes_table_to_column_metadata():
    spec = {
        "grai": {
            "edge_type": "TableToColumn",
            "edge_attributes": {},
        }
    }

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiEdgeMetadata)
    assert isinstance(obj.grai, GenericEdgeMetadataV1)
    assert isinstance(obj.grai, TableToColumnMetadata)
    assert isinstance(obj.grai.edge_attributes, TableToColumnAttributes)
