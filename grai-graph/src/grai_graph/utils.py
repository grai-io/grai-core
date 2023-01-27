from typing import Dict, List, Optional, Tuple, Union

from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnAttributes,
    ColumnToColumnMetadata,
    EdgeTypeLabels,
    GenericEdgeMetadataV1,
)
from grai_schemas.v1.metadata.nodes import (
    ColumnAttributes,
    ColumnMetadata,
    NodeTypeLabels,
)
from pydantic import BaseModel

from grai_graph import analysis, graph

DEFAULT_NAMESPACE = "test"


class TestNodeObj(BaseModel):
    name: str
    namespace: Optional[str] = DEFAULT_NAMESPACE
    node_attributes: Optional[ColumnAttributes] = None

    def __hash__(self):
        return hash((self.name, self.namespace))


def mock_v1_node(node: Union[str, TestNodeObj]):
    if isinstance(node, str):
        node = TestNodeObj(name=node)

    metadata = node.node_attributes if node.node_attributes is not None else {}
    node_dict = {
        "type": "Node",
        "version": "v1",
        "spec": {
            "id": None,
            "name": node.name,
            "namespace": node.namespace,
            "data_source": "test_source",
            "display_name": node.name,
            "is_active": True,
            "metadata": {
                "grai": ColumnMetadata(node_type=NodeTypeLabels.column.value, node_attributes=metadata).dict()
            },
        },
    }
    return NodeV1(**node_dict)


def mock_v1_edge(
    source_node: Union[str, TestNodeObj],
    destination_node: Union[str, TestNodeObj],
    metadata={},
):
    if isinstance(source_node, str):
        source_node = TestNodeObj(name=source_node)
    if isinstance(destination_node, str):
        destination_node = TestNodeObj(name=destination_node)

    edge_dict = {
        "type": "Edge",
        "version": "v1",
        "spec": {
            "id": None,
            "name": f"{source_node.namespace}.{source_node.name} -> {destination_node.namespace}.{destination_node.name}",
            "namespace": source_node.namespace,
            "data_source": "test_source",
            "source": {"name": source_node.name, "namespace": source_node.namespace},
            "destination": {
                "name": destination_node.name,
                "namespace": destination_node.namespace,
            },
            "is_active": True,
            "metadata": {
                "grai": ColumnToColumnMetadata(
                    edge_type=EdgeTypeLabels.column_to_column.value,
                    edge_attributes=metadata,
                ).dict()
            },
        },
    }
    return EdgeV1(**edge_dict)


def build_graph_from_map(map: Dict[Union[str, TestNodeObj], List[Tuple[str, ColumnToColumnAttributes]]]) -> graph.Graph:
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
    map: Dict[Union[str, TestNodeObj], Dict[ColumnToColumnAttributes, List[str]]]
) -> analysis.GraphAnalyzer:
    graph = build_graph_from_map(map)
    return analysis.GraphAnalyzer(graph)
