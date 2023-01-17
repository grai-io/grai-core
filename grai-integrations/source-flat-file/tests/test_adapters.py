import os

from grai_schemas import config as core_config
from grai_schemas.models import GraiEdgeMetadata, GraiNodeMetadata

from grai_source_flat_file.base import get_nodes_and_edges
from grai_source_flat_file.package_definitions import config


def test_metadata_has_core_metadata_ids(mock_get_nodes_and_edges):
    nodes, edges = mock_get_nodes_and_edges
    for node in nodes:
        assert core_config.metadata_id in node.spec.metadata

    for edge in edges:
        assert core_config.metadata_id in edge.spec.metadata


def test_metadata_has_dbt_metadata_id(mock_get_nodes_and_edges):
    nodes, edges = mock_get_nodes_and_edges
    for node in nodes:
        assert config.metadata_id in node.spec.metadata

    for edge in edges:
        assert config.metadata_id in edge.spec.metadata


def test_metadata_is_core_compliant(mock_get_nodes_and_edges):
    nodes, edges = mock_get_nodes_and_edges

    for node in nodes:
        assert isinstance(node.spec.metadata[core_config.metadata_id], GraiNodeMetadata)

    for edge in edges:
        assert isinstance(edge.spec.metadata[core_config.metadata_id], GraiEdgeMetadata)
