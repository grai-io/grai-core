import uuid
from typing import Union

import networkx as nx

from grai_graph.graph import Graph


class GraphAnalyzer:
    def __init__(self, graph: Graph):
        self.graph = graph

    def downstream_nodes(self, namespace: str, name: str):
        node_id = self.graph.get_node_id(namespace, name)
        downstream = list(nx.bfs_successors(self.graph.graph, node_id))[0][1]
        return [self.graph.get_node(node_id=node) for node in downstream]

    def test_delete_node(self, namespace: str, name: str):
        return list(self.downstream_nodes(namespace, name))

    def test_type_change(self, namespace: str, name: str, new_type: str):
        node_id = self.graph.get_node_id(namespace, name)
        current_node = self.graph.get_node(namespace, name)
        if 'data_type' in current_node.spec.metadata:
            current_type = current_node.spec.metadata['data_type']
            if current_type == new_type:
                return []
        else:
            raise AttributeError(f"No data type defined for {self.graph.id_label(node_id)}")
        result = self.graph.graph.successors(node_id)
        return [self.graph.get_node(node_id=node_id) for node_id in result]


