import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1
from grai_schemas.v1.metadata.edges import ColumnToColumnMetadata, TableToColumnMetadata
from grai_schemas.v1.metadata.nodes import ColumnMetadata, TableMetadata

from grai_source_redshift.adapters import adapt_to_client, build_grai_metadata
from grai_source_redshift.models import Column, ColumnID, Edge, Table, TableID
from grai_source_redshift.package_definitions import config

columns = [
    Column(
        name="test",
        namespace="tests",
        table="test",
        schema="test",
        data_type="integer",
        is_nullable=True,
        default_value="Orange",
        is_pk=True,
    )
]
column_values = [(item, "v1", SourcedNodeV1) for item in columns]


@pytest.mark.parametrize("item,version,target", column_values)
def test_column_adapter(item, version, target, mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, mock_source, version)
    assert isinstance(result, target)


table_types = ["BASE TABLE", "VIEW", "FOREIGN", "LOCAL TEMPORARY"]

tables = [
    Table(
        name="test",
        namespace="tests",
        table_schema="test",
        columns=[],
        metadata={"thing": "here"},
        table_type=table_type,
    )
    for table_type in table_types
]
table_values = [(item, "v1", SourcedNodeV1) for item in tables]


@pytest.mark.parametrize("item,version,target", table_values)
def test_table_adapter(item, version, target, mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, mock_source, version)
    assert isinstance(result, target), f"Adapter failed for {item}"


source = ColumnID(table_schema="schema", table_name="table", name="id", namespace="test")
destination = ColumnID(table_schema="schema", table_name="table", name="id2", namespace="test")
edges = [
    Edge(
        source=source,
        destination=destination,
        definition="thing",
        constraint_type="FOREIGN KEY",
    )
]
edge_values = [(item, "v1", SourcedEdgeV1) for item in edges]


def test_column_vs_edge_id():
    """ """
    from typing import Union

    from pydantic import BaseModel

    class Temp(BaseModel):
        """ """

        item: Union[ColumnID, TableID]

    data = {
        "table_name": "test",
        "table_schema": "test2",
        "name": "test3",
        "namespace": "test3",
    }
    result = Temp(item=data)
    assert isinstance(result.item, ColumnID)


@pytest.mark.xfail
def test_table_id_is_column_id():
    """ """
    data = {
        "table_name": "test",
        "table_schema": "test2",
        "name": "test3",
        "namespace": "test3",
    }
    TableID(**data)


def test_make_table_metadata():
    """ """
    metadata = build_grai_metadata(tables[0], "v1")
    assert isinstance(metadata, TableMetadata)


def test_make_column_metadata():
    """ """
    metadata = build_grai_metadata(columns[0], "v1")
    assert isinstance(metadata, ColumnMetadata)


def test_make_edge_metadata():
    """ """
    metadata = build_grai_metadata(edges[0], "v1")
    assert isinstance(metadata, ColumnToColumnMetadata)


@pytest.mark.parametrize("item,version,target", edge_values)
def test_edge_adapter(item, version, target, mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, mock_source, version)
    assert isinstance(result, target)


class TestAdapter:
    """ """

    # def test_all_node_full_names_unique(self, nodes):
    #     node_names = {node.full_name for node in nodes}
    #     assert len(node_names) == len(nodes)

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
        message = (
            "All edge sources should exist in the node list"
            f"Edge destinations {edge_source_ids - node_ids} missing from node list"
        )
        assert len(edge_source_ids - node_ids) == 0, message

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
        message = (
            "All edge destinations should exist in the node list"
            f"Edge destinations {edge_destination_ids - node_ids} missing from node list"
        )
        assert len(edge_destination_ids - node_ids) == 0, message

    def test_has_table_to_column_metadata(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert any(isinstance(edge.spec.metadata.grai, TableToColumnMetadata) for edge in edges)

    def test_has_column_to_column_metadata(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        assert any(isinstance(edge.spec.metadata.grai, ColumnToColumnMetadata) for edge in edges)

    def test_all_bt_edges_have_table_to_column_metadata(self, edges):
        """

        Args:
            edges:

        Returns:

        Raises:

        """
        bt_edges = (edge for edge in edges if edge.spec.metadata.grai_source_redshift["constraint_type"] == "bt")
        for edge in bt_edges:
            assert isinstance(edge.metadata.grai, TableToColumnMetadata)

    def test_metadata_has_core_metadata_ids(self, nodes_and_edges):
        """

        Args:
            nodes_and_edges:

        Returns:

        Raises:

        """
        nodes, edges = nodes_and_edges
        for node in nodes:
            assert hasattr(node.spec.metadata, core_config.metadata_id)

        for edge in edges:
            assert hasattr(edge.spec.metadata, core_config.metadata_id)

    def test_metadata_has_metadata_id(self, nodes_and_edges):
        """

        Args:
            nodes_and_edges:

        Returns:

        Raises:

        """
        nodes, edges = nodes_and_edges
        for node in nodes:
            assert hasattr(node.spec.metadata, config.metadata_id)

        for edge in edges:
            assert hasattr(edge.spec.metadata, config.metadata_id)

    def test_metadata_is_core_compliant(self, nodes_and_edges):
        """

        Args:
            nodes_and_edges:

        Returns:

        Raises:

        """
        nodes, edges = nodes_and_edges

        for node in nodes:
            assert isinstance(
                getattr(node.spec.metadata, core_config.metadata_id), GraiNodeMetadataV1
            ), node.spec.metadata

        for edge in edges:
            assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), GraiEdgeMetadataV1)
