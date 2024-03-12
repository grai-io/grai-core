import random
from functools import cached_property

from grai_schemas import config as core_config
from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1
from grai_source_cube.adapters import adapt_to_client
from grai_source_cube.mock_tools import (
    CubeEdgeColumnToColumnFactory,
    CubeEdgeTableToColumnFactory,
    CubeEdgeTableToTableFactory,
    CubeNodeFactory,
    DimensionNodeFactory,
    MeasureNodeFactory,
    SourceColumnNodeFactory,
    SourceTableNodeFactory,
)


class AdapterTestGenerators:
    """ """

    column_generators = [
        SourceColumnNodeFactory.build,
        DimensionNodeFactory.build,
        MeasureNodeFactory.build,
    ]

    table_generators = [
        CubeNodeFactory.build,
        SourceTableNodeFactory.build,
    ]

    edge_generators = [
        CubeEdgeTableToColumnFactory.build,
        CubeEdgeTableToTableFactory.build,
        CubeEdgeColumnToColumnFactory.build,
    ]

    @cached_property
    def columns(self) -> list:
        """ """
        return [random.choice(self.column_generators)() for _ in range(1000)]

    @cached_property
    def tables(self) -> list:
        """ """
        return [random.choice(self.table_generators)() for _ in range(1000)]

    @cached_property
    def edges(self) -> list:
        """ """
        return [random.choice(self.edge_generators)() for _ in range(1000)]


AdapterTestValues = AdapterTestGenerators()


def test_adapted_columns_are_sourced(mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(AdapterTestValues.columns, mock_source, "v1")
    for item in result:
        assert isinstance(item, SourcedNodeV1), f"Adapted column:\n`{pprint(item)}` is not sourced"


def test_adapted_table_are_sourced(mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(AdapterTestValues.tables, mock_source, "v1")
    for item in result:
        assert isinstance(item, SourcedNodeV1), f"Received a node of type {type(item)} expecting a SourcedNodeV1"


def test_adapted_edges_are_sourced(mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(AdapterTestValues.edges, mock_source, "v1")
    for item in result:
        assert isinstance(item, SourcedEdgeV1), f"Received an edge of type {type(item)} expecting a SourcedEdgeV1"


def test_node_metadata_has_core_metadata_ids(nodes):
    """

    Args:
        nodes:

    Returns:

    Raises:

    """
    for node in nodes:
        assert hasattr(node.spec.metadata, core_config.metadata_id)


def test_edge_metadata_has_core_metadata_ids(edges):
    """

    Args:
        edges:

    Returns:

    Raises:

    """
    for edge in edges:
        assert hasattr(edge.spec.metadata, core_config.metadata_id)


def test_node_metadata_is_core_compliant(nodes):
    """

    Args:
        nodes:

    Returns:

    Raises:

    """
    for node in nodes:
        assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), GraiNodeMetadataV1)


def test_edge_metadata_is_core_compliant(edges):
    """

    Args:
        edges:

    Returns:

    Raises:

    """
    for edge in edges:
        assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), GraiEdgeMetadataV1)
