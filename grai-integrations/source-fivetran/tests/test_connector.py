import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata.edges import ColumnToColumnMetadata
from grai_schemas.v1.metadata.edges import Metadata as EdgeV1Metadata
from grai_schemas.v1.metadata.edges import TableToColumnMetadata, TableToTableMetadata
from grai_schemas.v1.metadata.nodes import ColumnMetadata
from grai_schemas.v1.metadata.nodes import Metadata as NodeV1Metadata
from grai_schemas.v1.metadata.nodes import NodeTypeLabels, TableMetadata

from grai_source_fivetran.loader import FivetranConnector, build_namespace_map
from grai_source_fivetran.models import Edge, NodeTypes
from grai_source_fivetran.package_definitions import config


def test_loader_node_types(app_nodes):
    """

    Args:
        app_nodes:

    Returns:

    Raises:

    """
    assert all(isinstance(node, NodeTypes) for node in app_nodes)


def test_loader_edge_types(app_edges):
    """

    Args:
        app_edges:

    Returns:

    Raises:

    """
    assert all(isinstance(edge, Edge) for edge in app_edges)


class TestNamespaceMap:
    """ """

    def test_namespace_map_from_json(self):
        """ """
        json_str = '{"conn_id": {"source": "test_source", "destination": "test_destination"}}'
        namespace_map = build_namespace_map({}, json_str, "temp")
        assert len(namespace_map.keys()) > 0

    @pytest.mark.xfail
    def test_namespace_map_from_invalid_json(self):
        """ """
        json_str = "'test'"
        namespace_map = build_namespace_map({}, json_str, "temp")
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
        test_type = NodeV1
        for item in nodes:
            assert isinstance(item, test_type), f"{type(item)} is not of type {test_type}"

    def test_v1_adapt_edges(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        test_type = EdgeV1
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

    def test_has_table_to_column_metadata(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert any(isinstance(edge.spec.metadata.grai, TableToColumnMetadata) for edge in edges)

    def test_has_table_to_table_metadata(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert any(isinstance(edge.spec.metadata.grai, TableToTableMetadata) for edge in edges)

    def test_all_bt_edges_have_table_to_column_metadata(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        bt_edges = (edge for edge in edges if edge.spec.metadata.grai_source_fivetran["constraint_type"] == "bt")
        for edge in bt_edges:
            assert isinstance(edge.metadata.grai, TableToColumnMetadata)

    def test_all_dbtm_edges_have_column_to_column_metadata(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        bt_edges = (edge for edge in edges if edge.spec.metadata.grai_source_fivetran["constraint_type"] == "dbtm")
        for edge in bt_edges:
            assert isinstance(edge.metadata.grai, ColumnToColumnMetadata)

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

    def test_metadata_has_dbt_metadata_id(self, nodes, edges):
        """

        Args:
            nodes:
            edges:

        Returns:

        Raises:

        """
        for node in nodes:
            assert hasattr(node.spec.metadata, config.metadata_id)

        for edge in edges:
            assert hasattr(edge.spec.metadata, config.metadata_id)

    def test_metadata_is_core_compliant(self, nodes, edges):
        """

        Args:
            nodes:
            edges:

        Returns:

        Raises:

        """
        for node in nodes:
            assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), NodeV1Metadata), node.spec.metadata

        for edge in edges:
            assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), EdgeV1Metadata)
