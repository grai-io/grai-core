from typing import get_args

import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.metadata.edges import GenericEdgeMetadataV1
from grai_schemas.v1.metadata.edges import Metadata as EdgeV1Metadata
from grai_schemas.v1.metadata.nodes import Metadata as NodeV1Metadata

from grai_source_metabase.loader import MetabaseConnector, build_namespace_map
from grai_source_metabase.models import Edge, NodeTypes


def test_loader_node_types(app_nodes):
    """

    Args:
        app_nodes:

    Returns:

    Raises:

    """

    assert all(isinstance(node, get_args(NodeTypes)) for node in app_nodes)


def test_loader_edge_types(app_edges):
    """

    Args:
        app_edges:

    Returns:

    Raises:

    """
    assert all(isinstance(edge, Edge) for edge in app_edges)


class TestBuildNamespaceMap:
    """ """

    def test_namespace_map_from_json(self):
        """ """
        test_dict = {2: {"name": "test_destination"}}
        namespace_map = build_namespace_map({1: "B"}, test_dict, "temp")
        assert len(namespace_map.keys()) > 0

    @pytest.mark.xfail
    def test_namespace_map_from_invalid_json(self):
        """ """
        test_dict = {2: {"name": "test_destination"}}
        namespace_map = build_namespace_map({}, test_dict, "temp")
        assert len(namespace_map.keys()) > 0


class TestConnector:
    """ """

    def test_graph_nodes_created(self, nodes):
        """

        Args:
            nodes:

        Returns:

        Raises:

        """
        assert len(nodes) > 0

    def test_graph_edges_created(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert len(edges) > 0

    def test_all_manifest_node_full_names_unique(self, nodes):
        """

        Args:
            nodes:

        Returns:

        Raises:

        """
        node_names = {node for node in nodes}
        assert len(node_names) == len(nodes)

    def test_all_manifest_edge_full_names_unique(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        node_names = {edge for edge in edges}
        assert len(node_names) == len(edges)

    def test_v1_adapted_nodes_have_name(self, nodes):
        """

        Args:
            nodes:

        Returns:

        Raises:

        """
        assert all(node.spec.name is not None for node in nodes)

    def test_v1_adapted_nodes_have_namespace(self, nodes):
        """

        Args:
            nodes:

        Returns:

        Raises:

        """
        assert all(node.spec.namespace is not None for node in nodes)

    def test_v1_adapted_edge_source_has_name(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert all(edge.spec.source.name is not None for edge in edges)

    def test_v1_adapted_edge_source_has_namespace(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert all(edge.spec.source.namespace is not None for edge in edges)

    def test_v1_adapted_edge_destination_has_name(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert all(edge.spec.destination.name is not None for edge in edges)

    def test_v1_adapted_edge_destination_has_namespace(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert all(edge.spec.destination.namespace is not None for edge in edges)

    def test_v1_adapt_nodes(self, nodes):
        """

        Args:
            nodes:

        Returns:

        Raises:

        """
        test_type = SourcedNodeV1
        for item in nodes:
            assert isinstance(item, test_type), f"{type(item)} is not of type {test_type}"

    def test_v1_adapt_edges(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        test_type = SourcedEdgeV1
        for item in edges:
            assert isinstance(item, test_type), f"{type(item)} is not of type {test_type}"

    def test_v1_adapted_edge_sources_have_nodes(self, nodes, edges):
        """

        Args:
            nodes:
            edges:

        Returns:

        Raises:

        """
        node_ids = {(n.spec.namespace, n.spec.name) for n in nodes}
        edge_source_ids = {(n.spec.source.namespace, n.spec.source.name) for n in edges}
        assert len(edge_source_ids - node_ids) == 0, "All edge sources should exist in the node list"

    def test_v1_adapted_edge_destination_have_nodes(self, nodes, edges):
        """

        Args:
            nodes:
            edges:

        Returns:

        Raises:

        """
        node_ids = {(n.spec.namespace, n.spec.name) for n in nodes}
        edge_destination_ids = {(n.spec.destination.namespace, n.spec.destination.name) for n in edges}
        assert len(edge_destination_ids - node_ids) == 0, "All edge destinations should exist in the node list"

    def test_has_table_to_question_metadata(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert all(isinstance(edge.spec.metadata.grai, GenericEdgeMetadataV1) for edge in edges)

    def test_metadata_has_core_metadata_ids(self, nodes, edges):
        """

        Args:
            nodes:
            edges:

        Returns:

        Raises:

        """
        for node in nodes:
            assert hasattr(node.spec.metadata, core_config.metadata_id)

        for edge in edges:
            assert hasattr(edge.spec.metadata, core_config.metadata_id)

    def test_metadata_is_core_compliant(self, nodes, edges):
        """

        Args:
            nodes:
            edges:

        Returns:

        Raises:

        """
        for node in nodes:
            assert isinstance(
                getattr(node.spec.metadata, core_config.metadata_id), get_args(NodeV1Metadata)
            ), node.spec.metadata

        for edge in edges:
            assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), get_args(EdgeV1Metadata))
