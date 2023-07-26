import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.metadata.edges import ColumnToColumnMetadata
from grai_schemas.v1.metadata.edges import Metadata as EdgeV1Metadata
from grai_schemas.v1.metadata.edges import TableToColumnMetadata, TableToTableMetadata
from grai_schemas.v1.metadata.nodes import Metadata as NodeV1Metadata

from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.data_tools import get_project_root
from grai_source_dbt.loaders import SUPPORTED_VERSIONS
from grai_source_dbt.package_definitions import config
from grai_source_dbt.processor import ManifestProcessor
from grai_source_dbt.utils import full_name


def resource_path(filename: str, version: str, subproject: str = "jaffle_shop"):
    """

    Args:
        filename (str):
        version (str):
        subproject (str, optional):  (Default value = "jaffle_shop")

    Returns:

    Raises:

    """
    file = f"{get_project_root()}/../tests/resources/{version}/{subproject}/{filename}"
    return file


def load_resource(file, source) -> ManifestProcessor:
    """

    Args:
        file:

    Returns:

    Raises:

    """
    return ManifestProcessor.load(file, "default", source)


files = [resource_path("manifest.json", ver) for ver in SUPPORTED_VERSIONS]
files += [
    resource_path("manifest-seed.json", "v8"),
    resource_path("manifest-snapshot.json", "v8"),
]
ids = SUPPORTED_VERSIONS + ["v8-seed", "v8-manifest"]


@pytest.mark.parametrize("file", files, ids=ids)
class TestProcessors:
    """ """

    def test_all_manifest_node_full_names_unique(self, file, mock_source):
        """"""
        processor = load_resource(file, mock_source)
        node_names = {full_name(node) for node in processor.manifest.nodes.values()}
        assert len(node_names) == len(processor.manifest.nodes)

    def test_all_manifest_source_full_names_unique(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        node_names = {full_name(node) for node in processor.manifest.sources.values()}
        assert len(node_names) == len(processor.manifest.sources)

    def test_all_manifest_source_and_node_full_names_unique(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        node_names = {full_name(node) for node in processor.manifest.nodes.values()}
        source_names = {full_name(node) for node in processor.manifest.sources.values()}
        assert (len(node_names) + len(source_names)) == (
            len(processor.manifest.nodes) + len(processor.manifest.sources)
        )

    def test_all_manifest_node_and_column_full_names_unique(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        node_names = {full_name(node) for node in processor.manifest.nodes.values()}
        column_names = {column.full_name for column in processor.loader.columns.values()}
        assert (len(node_names) + len(column_names)) == (len(processor.manifest.nodes) + len(processor.loader.columns))

    def test_graph_nodes_created(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert len(processor.nodes) > 0

    def test_graph_edges_created(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert len(processor.edges) > 0

    def validate_adapter_for_node_types(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        seen_types = []
        for node in processor.nodes.values():
            node_type = type(node)
            try:
                adapt_to_client(node, "v1")
            except:
                raise Exception(f"Failed to adapt node type: {node_type}")

    def validate_adapter_for_edge_types(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        seen_types = []
        for edge in processor.edges.values():
            edge_type = type(edge)
            try:
                adapt_to_client(edge, "v1")
            except:
                raise Exception(f"Failed to adapt node type: {edge_type}")

    def test_v1_adapted_nodes_have_name(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert all(node.spec.name is not None for node in processor.adapted_nodes)

    def test_v1_adapted_nodes_have_namespace(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert all(node.spec.namespace is not None for node in processor.adapted_nodes)

    def test_v1_adapted_edge_source_has_name(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert all(edge.spec.source.name is not None for edge in processor.adapted_edges)

    def test_v1_adapted_edge_source_has_namespace(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert all(edge.spec.source.namespace is not None for edge in processor.adapted_edges)

    def test_v1_adapted_edge_destination_has_name(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert all(edge.spec.destination.name is not None for edge in processor.adapted_edges)

    def test_v1_adapted_edge_destination_has_namespace(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert all(edge.spec.destination.namespace is not None for edge in processor.adapted_edges)

    def test_v1_adapt_nodes(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        test_type = SourcedNodeV1
        for item in processor.adapted_nodes:
            assert isinstance(item, test_type), f"{type(item)} is not of type {test_type}"

    def test_v1_adapt_edges(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        test_type = SourcedEdgeV1
        for item in processor.adapted_edges:
            assert isinstance(item, test_type), f"{type(item)} is not of type {test_type}"

    def test_v1_adapted_edge_sources_have_nodes(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        node_ids = {(n.spec.namespace, n.spec.name) for n in processor.adapted_nodes}
        edge_source_ids = {(n.spec.source.namespace, n.spec.source.name) for n in processor.adapted_edges}
        assert len(edge_source_ids - node_ids) == 0, "All edge sources should exist in the node list"

    def test_v1_adapted_edge_destination_have_nodes(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        node_ids = {(n.spec.namespace, n.spec.name) for n in processor.adapted_nodes}
        edge_destination_ids = {
            (n.spec.destination.namespace, n.spec.destination.name) for n in processor.adapted_edges
        }
        assert len(edge_destination_ids - node_ids) == 0, "All edge destinations should exist in the node list"

    def test_get_nodes_and_edges(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        nodes, edges = processor.adapted_nodes, processor.adapted_edges

        node_ids = {(node.spec.name, node.spec.namespace) for node in nodes}
        source_ids = {(e.spec.source.name, e.spec.source.namespace) for e in edges}
        destination_ids = {(e.spec.destination.name, e.spec.destination.namespace) for e in edges}

        assert len(source_ids - node_ids) == 0, f"Edge sources {source_ids - node_ids} missing from node list"
        assert (
            len(destination_ids - node_ids) == 0
        ), f"Edge destinations {destination_ids - node_ids} missing from node list"

    def test_has_table_to_column_metadata(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert any(isinstance(edge.spec.metadata.grai, TableToColumnMetadata) for edge in processor.adapted_edges)

    def test_has_table_to_table_metadata(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        assert any(isinstance(edge.spec.metadata.grai, TableToTableMetadata) for edge in processor.adapted_edges)

    def test_all_bt_edges_have_table_to_column_metadata(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        bt_edges = (edge for edge in processor.adapted_edges if edge.spec.metadata.constraint_type == "bt")
        for edge in bt_edges:
            assert isinstance(edge.metadata.grai, TableToColumnMetadata)

    def test_all_dbtm_edges_have_column_to_column_metadata(self, file, mock_source):
        """

        Args:
            processor:

        Returns:

        Raises:

        """
        processor = load_resource(file, mock_source)
        bt_edges = (edge for edge in processor.adapted_edges if edge.spec.metadata.constraint_type == "dbtm")
        for edge in bt_edges:
            assert isinstance(edge.metadata.grai, ColumnToColumnMetadata)

    # def test_metadata_has_core_metadata_ids(self, file, mock_source):
    #     """
    #
    #     Args:
    #         processor:
    #
    #     Returns:
    #
    #     Raises:
    #
    #     """
    #     processor = load_resource(file, mock_source)
    #     nodes, edges = processor.adapted_nodes, processor.adapted_edges
    #     for node in nodes:
    #         assert hasattr(node.spec.metadata, core_config.metadata_id)
    #
    #     for edge in edges:
    #         assert hasattr(edge.spec.metadata, core_config.metadata_id)
    #
    # def test_metadata_has_dbt_metadata_id(self, file, mock_source):
    #     """
    #
    #     Args:
    #         processor:
    #
    #     Returns:
    #
    #     Raises:
    #
    #     """
    #     processor = load_resource(file, mock_source)
    #     nodes, edges = processor.adapted_nodes, processor.adapted_edges
    #     for node in nodes:
    #         assert hasattr(node.spec.metadata, config.metadata_id)
    #
    #     for edge in edges:
    #         assert hasattr(edge.spec.metadata, config.metadata_id)
    #
    # def test_metadata_is_core_compliant(self, file, mock_source):
    #     """
    #
    #     Args:
    #         processor:
    #
    #     Returns:
    #
    #     Raises:
    #
    #     """
    #     processor = load_resource(file, mock_source)
    #     nodes, edges = processor.adapted_nodes, processor.adapted_edges
    #
    #     for node in nodes:
    #         assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), NodeV1Metadata), node.spec.metadata
    #
    #     for edge in edges:
    #         assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), EdgeV1Metadata)
