from grai_schemas.base import Metadata
from grai_schemas.models import (
    ColumnMetadata,
    ColumnToColumnAttributes,
    GraiEdgeMetadata,
    TableMetadata,
)


def test_distinguishes_column_metadata():
    spec = {
        "grai": {"node_type": "Column", "node_attributes": {"is_primary_key": True}}
    }

    obj = Metadata(**spec)
    assert isinstance(obj.grai, ColumnMetadata)


def test_distinguishes_table_metadata():
    spec = {"grai": {"node_type": "Table", "node_attributes": {"is_primary_key": True}}}

    obj = Metadata(**spec)
    assert isinstance(obj.grai, TableMetadata)


def test_distinguishes_edge_metadata():
    spec = {
        "grai": {
            "edge_type": "ColumnToColumn",
            "edge_attributes": {"preserves_unique": True},
        }
    }

    obj = Metadata(**spec)
    assert isinstance(obj.grai, GraiEdgeMetadata)


def test_distinguishes_column_to_column_attributes():
    spec = {
        "grai": {
            "edge_type": "ColumnToColumn",
            "edge_attributes": {"preserves_unique": True},
        }
    }

    obj = Metadata(**spec)
    assert isinstance(obj.grai.edge_attributes, ColumnToColumnAttributes)
