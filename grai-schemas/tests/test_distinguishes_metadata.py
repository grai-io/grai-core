from grai_schemas.base import EdgeMetadata, NodeMetadata
from grai_schemas.models import (
    ColumnMetadata,
    ColumnToColumnAttributes,
    EdgeV1,
    GraiEdgeMetadata,
    NodeV1,
    TableMetadata,
)


def test_distinguishes_column_metadata():
    spec = {
        "grai": {"node_type": "Column", "node_attributes": {"is_primary_key": True}}
    }

    obj = NodeMetadata(**spec)
    assert isinstance(obj.grai, ColumnMetadata)


def test_distinguishes_table_metadata():
    spec = {"grai": {"node_type": "Table", "node_attributes": {"is_primary_key": True}}}

    obj = NodeMetadata(**spec)
    assert isinstance(obj.grai, TableMetadata)


def test_distinguishes_table_metadata():
    spec = {"grai": {"node_type": "Table", "node_attributes": {"is_primary_key": True}}}

    obj = NodeMetadata(**spec)
    assert isinstance(obj.grai, NodeV1)


def test_distinguishes_edge_metadata():
    spec = {
        "grai": {
            "edge_type": "ColumnToColumn",
            "edge_attributes": {"preserves_unique": True},
        }
    }

    obj = EdgeMetadata(**spec)
    assert isinstance(obj.grai, EdgeV1)


def test_distinguishes_column_to_column_attributes():
    spec = {
        "grai": {
            "edge_type": "ColumnToColumn",
            "edge_attributes": {"preserves_unique": True},
        }
    }

    obj = EdgeMetadata(**spec)
    assert isinstance(obj.grai.edge_attributes, ColumnToColumnAttributes), obj.grai


def test_handles_extra_metadata():
    spec = {
        "grai": {
            "edge_type": "ColumnToColumn",
            "edge_attributes": {"preserves_unique": True},
        },
        "random_stuff": {},
    }

    obj = EdgeMetadata(**spec)
    assert isinstance(obj.grai.edge_attributes, ColumnToColumnAttributes)
