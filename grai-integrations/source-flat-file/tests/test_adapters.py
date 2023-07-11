import os

from grai_schemas import config as core_config
from grai_schemas.v1.metadata.edges import Metadata as EdgeV1Metadata
from grai_schemas.v1.metadata.nodes import Metadata as NodeV1Metadata

from grai_source_flat_file.package_definitions import config


def test_metadata_has_core_metadata_ids(mock_get_nodes_and_edges):
    """

    Args:
        mock_get_nodes_and_edges:

    Returns:

    Raises:

    """
    nodes, edges = mock_get_nodes_and_edges
    for node in nodes:
        assert hasattr(node.spec.metadata, core_config.metadata_id)

    for edge in edges:
        assert hasattr(edge.spec.metadata, core_config.metadata_id)


def test_metadata_has_flat_file_metadata_id(mock_get_nodes_and_edges):
    """

    Args:
        mock_get_nodes_and_edges:

    Returns:

    Raises:

    """
    nodes, edges = mock_get_nodes_and_edges
    for node in nodes:
        assert hasattr(node.spec.metadata, config.metadata_id)

    for edge in edges:
        assert hasattr(edge.spec.metadata, config.metadata_id)


def test_metadata_is_core_compliant(mock_get_nodes_and_edges):
    """

    Args:
        mock_get_nodes_and_edges:

    Returns:

    Raises:

    """
    nodes, edges = mock_get_nodes_and_edges

    for node in nodes:
        assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), NodeV1Metadata)

    for edge in edges:
        assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), EdgeV1Metadata)
