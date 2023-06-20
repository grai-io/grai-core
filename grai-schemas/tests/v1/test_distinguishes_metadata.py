from typing import Dict

from grai_schemas.base import GraiMetadata
from grai_schemas.generics import MalformedMetadata
from grai_schemas.v1.metadata.edges import (
    BaseEdgeMetadataV1,
    ColumnToColumnAttributes,
    ColumnToColumnMetadata,
    GenericEdgeMetadataV1,
    MalformedEdgeMetadataV1,
)
from grai_schemas.v1.metadata.edges import Metadata as GraiEdgeMetadata
from grai_schemas.v1.metadata.edges import (
    TableToColumnAttributes,
    TableToColumnMetadata,
)
from grai_schemas.v1.metadata.generics import GenericAttributes
from grai_schemas.v1.metadata.metadata import (
    GraiMalformedEdgeMetadataV1,
    GraiMalformedNodeMetadataV1,
    MetadataV1,
)
from grai_schemas.v1.metadata.nodes import (
    BaseNodeMetadataV1,
    ColumnAttributes,
    ColumnMetadata,
    GenericNodeMetadataV1,
    MalformedNodeMetadataV1,
)
from grai_schemas.v1.metadata.nodes import Metadata as GraiNodeMetadata
from grai_schemas.v1.metadata.nodes import TableAttributes, TableMetadata


def test_distinguishes_generic_node_metadata():
    """ """
    spec = {"grai": {"node_type": "Generic", "node_attributes": {}}}

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiNodeMetadata)
    assert isinstance(obj.grai, GenericNodeMetadataV1)
    assert isinstance(obj.grai.node_attributes, GenericAttributes)


class TestMalformedMetadata:
    def test_handle_malformed_generic_node(self):
        """ """
        spec = {"grai": {"node_type": "Purple"}}

        obj = MalformedMetadata(**spec)
        assert isinstance(obj, MalformedMetadata)
        assert obj.malformed_values == spec

    def test_handle_malformed_node(self):
        """ """
        spec = {"grai": {"node_type": "Purple"}}

        obj = MalformedNodeMetadataV1(**spec)
        assert isinstance(obj, MalformedMetadata)
        assert hasattr(obj, "node_type")
        assert obj.node_type == "Malformed"
        assert obj.malformed_values == spec

    def test_handle_malformed_grai_node(self):
        """ """
        spec = {"test": {"node_type": "Purple"}}

        obj = GraiMalformedNodeMetadataV1(**spec)
        assert isinstance(obj, MalformedMetadata)
        assert isinstance(obj, MetadataV1)
        assert hasattr(obj, "grai")
        assert isinstance(obj.grai, MalformedNodeMetadataV1)
        assert obj.malformed_values == spec

    def test_handle_malformed_generic_edge(self):
        """ """
        spec = {"grai": {"edge_type": "Lavender"}}

        obj = MalformedMetadata(**spec)
        assert isinstance(obj, MalformedMetadata)
        assert obj.malformed_values == spec

    def test_handle_malformed_edge(self):
        """ """
        spec = {"grai": {"edge_type": "Lavender"}}

        obj = MalformedEdgeMetadataV1(**spec)
        assert isinstance(obj, MalformedMetadata)
        assert hasattr(obj, "edge_type")
        assert obj.edge_type == "Malformed"
        assert obj.malformed_values == spec

    def test_handle_missing_grai_metadata(self):
        """ """
        spec = {}

        obj = MalformedMetadata(**spec)
        assert isinstance(obj, MalformedMetadata)
        assert obj.malformed_values == spec

    def test_handle_malformed_grai_edge(self):
        """ """
        spec = {"test": {"edge_type": "Purple"}}

        obj = GraiMalformedEdgeMetadataV1(**spec)
        assert isinstance(obj, MalformedMetadata)
        assert isinstance(obj, MetadataV1)
        assert hasattr(obj, "grai")
        assert isinstance(obj.grai, MalformedEdgeMetadataV1)
        assert obj.malformed_values == spec


def test_distinguishes_column_metadata():
    """ """
    spec = {"grai": {"node_type": "Column", "node_attributes": {"is_primary_key": True}}}

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiNodeMetadata)
    assert isinstance(obj.grai, BaseNodeMetadataV1)
    assert isinstance(obj.grai, ColumnMetadata)
    assert isinstance(obj.grai.node_attributes, ColumnAttributes)


def test_distinguishes_table_metadata():
    """ """
    spec = {"grai": {"node_type": "Table", "node_attributes": {"is_primary_key": True}}}

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiNodeMetadata)
    assert isinstance(obj.grai, BaseNodeMetadataV1)
    assert isinstance(obj.grai, TableMetadata)
    assert isinstance(obj.grai.node_attributes, TableAttributes)


def test_distinguishes_generic_edge_metadata():
    """ """
    spec = {
        "grai": {
            "edge_type": "Generic",
            "edge_attributes": {},
        }
    }

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiEdgeMetadata)
    assert isinstance(obj.grai, GenericEdgeMetadataV1)
    assert isinstance(obj.grai.edge_attributes, GenericAttributes)


def test_distinguishes_column_to_column_metadata():
    """ """
    spec = {
        "grai": {
            "edge_type": "ColumnToColumn",
            "edge_attributes": {"preserves_unique": True},
        }
    }

    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiEdgeMetadata)
    assert isinstance(obj.grai, BaseEdgeMetadataV1)
    assert isinstance(obj.grai, ColumnToColumnMetadata)
    assert isinstance(obj.grai.edge_attributes, ColumnToColumnAttributes)


def test_metadata_distinguishes_table_to_column_metadata():
    """ """
    spec = {
        "grai": {
            "edge_type": "TableToColumn",
            "edge_attributes": {},
        }
    }
    obj = GraiMetadata(**spec)
    assert isinstance(obj.grai, GraiEdgeMetadata)
    assert isinstance(obj.grai, BaseEdgeMetadataV1)
    assert isinstance(obj.grai, TableToColumnMetadata)
    assert isinstance(obj.grai.edge_attributes, TableToColumnAttributes)
