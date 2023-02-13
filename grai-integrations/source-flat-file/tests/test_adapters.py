import os

from grai_schemas import config as core_config
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1

from grai_source_flat_file.base import get_nodes_and_edges
from grai_source_flat_file.package_definitions import config


def test_metadata_has_core_metadata_ids(mock_get_nodes_and_edges):
    nodes, edges = mock_get_nodes_and_edges
    for node in nodes:
        assert hasattr(node.spec.metadata, core_config.metadata_id)

    for edge in edges:
        assert hasattr(edge.spec.metadata, core_config.metadata_id)


def test_metadata_has_flat_file_metadata_id(mock_get_nodes_and_edges):
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
