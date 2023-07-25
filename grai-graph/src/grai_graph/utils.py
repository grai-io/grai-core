from typing import Any, Dict, List, Optional, Tuple, Union

from grai_schemas.v1 import EdgeV1, NodeV1, mock
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnAttributes,
    ColumnToColumnMetadata,
    EdgeMetadataTypeLabels,
    GenericEdgeMetadataV1,
)
from grai_schemas.v1.metadata.metadata import NodeMetadataV1
from grai_schemas.v1.metadata.nodes import (
    ColumnAttributes,
    ColumnMetadata,
    NodeMetadataTypeLabels,
)
from grai_schemas.v1.node import NamedSpec
from pydantic import BaseModel

from grai_graph import analysis, graph

DEFAULT_NAMESPACE = "test"


class TestNodeObj(BaseModel):
    """ """

    name: str
    namespace: Optional[str] = DEFAULT_NAMESPACE
    node_attributes: Optional[ColumnAttributes] = None
    data_sources: List[Any] = []

    def __hash__(self):
        return hash((self.name, self.namespace))


def mock_v1_node(node: Union[str, TestNodeObj]):
    """

    Args:
        node (Union[str, TestNodeObj]):

    Returns:

    Raises:

    """
    if isinstance(node, str):
        node = TestNodeObj(name=node)

    node_attributes = node.node_attributes if node.node_attributes is not None else {}
    metadata = {
        "grai": ColumnMetadata(
            node_type=NodeMetadataTypeLabels.column.value,
            node_attributes=node_attributes,
        ),
        "sources": {},
    }

    node_spec = mock.MockV1().node.named_node_spec(
        id=None,
        name=node.name,
        namespace=node.namespace,
        data_source="test_source",
        is_active=True,
        metadata=metadata,
    )
    node = NodeV1.from_spec(node_spec)
    node.spec.metadata = metadata

    return node


def mock_v1_edge(
    source_node: Union[str, TestNodeObj],
    destination_node: Union[str, TestNodeObj],
    metadata={},
):
    """

    Args:
        source_node (Union[str, TestNodeObj]):
        destination_node (Union[str, TestNodeObj]):
        metadata:  (Default value = {})

    Returns:

    Raises:

    """
    if isinstance(source_node, str):
        source_node = TestNodeObj(name=source_node)
    if isinstance(destination_node, str):
        destination_node = TestNodeObj(name=destination_node)

    metadata = {
        "grai": ColumnToColumnMetadata(
            edge_type=EdgeMetadataTypeLabels.column_to_column.value,
            edge_attributes=metadata,
        ),
        "sources": [],
    }
    name = f"{source_node.namespace}.{source_node.name} -> {destination_node.namespace}.{destination_node.name}"

    node_metadata: NodeMetadataV1 = {
        "grai": ColumnMetadata(
            node_type="Column",
            node_attributes={},
        ).dict(),
    }

    edge_spec = mock.MockV1().edge.named_edge_spec(
        id=None,
        name=name,
        namespace=source_node.namespace,
        source=NamedSpec(**source_node.dict(), metadata=node_metadata),
        destination=NamedSpec(**destination_node.dict(), metadata=node_metadata),
        is_active=True,
        metadata=metadata,
    )
    edge = EdgeV1.from_spec(edge_spec)
    edge.spec.metadata = metadata
    return edge


def build_graph_from_map(map: Dict[Union[str, TestNodeObj], List[Tuple[str, ColumnToColumnAttributes]]]) -> graph.Graph:
    """

    Args:
        map (Dict[Union[str, TestNodeObj]):
        List]]]:

    Returns:

    Raises:

    """
    nodes = [node if isinstance(node, TestNodeObj) else TestNodeObj(name=node) for node in map.keys()]
    node_name_map = {node.name: node for node in nodes}
    nodes = [mock_v1_node(node) for node in nodes]

    edges = (
        (source, node_name_map[destination], meta)
        for source, dest_meta in map.items()
        for destination, meta in dest_meta
    )
    edges = [mock_v1_edge(*args) for args in edges]
    return graph.build_graph(nodes, edges, "v1")


def get_analysis_from_map(
    map: Dict[Union[str, TestNodeObj], List[Tuple[str, ColumnToColumnAttributes]]]
) -> analysis.GraphAnalyzer:
    """

    Args:
        map (Dict[Union[str, TestNodeObj]):
        Dict]]]:

    Returns:

    Raises:

    """
    graph = build_graph_from_map(map)
    return analysis.GraphAnalyzer(graph)
