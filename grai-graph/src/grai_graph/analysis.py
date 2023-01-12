import uuid
from typing import List, Optional, Union

import networkx as nx
from grai_client.schemas.node import NodeTypes

from grai_graph.graph import Graph


def get_is_unique(node: NodeTypes) -> Optional[bool]:
    return node.spec.metadata["grai"].get("node_attributes", {}).get("is_unique", None)


class GraphAnalyzer:
    def __init__(self, graph: Graph):
        self.graph = graph

    def downstream_nodes(self, namespace: str, name: str):
        node_id = self.graph.get_node_id(namespace, name)
        downstream = list(nx.bfs_successors(self.graph.graph, node_id))[0][1]
        return [self.graph.get_node(node_id=node) for node in downstream]

    def upstream_nodes(self, namespace: str, name: str):
        node_id = self.graph.get_node_id(namespace, name)
        upstream = list(nx.bfs_predecessors(self.graph.graph, node_id))[0][1]
        return [self.graph.get_node(node_id=node) for node in upstream]

    def test_delete_node(self, namespace: str, name: str):
        return list(self.downstream_nodes(namespace, name))

    def test_type_change(
        self, namespace: str, name: str, new_type: str
    ) -> List[NodeTypes]:
        """Returns a list of nodes affected by a type change

        :param namespace:
        :param name:
        :param new_type:
        :return:
        """
        node_id = self.graph.get_node_id(namespace, name)
        current_node = self.graph.get_node(namespace, name)

        if "data_type" in current_node.spec.metadata["grai"].get("node_attributes", {}):
            current_type = current_node.spec.metadata["grai"]["node_attributes"][
                "data_type"
            ]

            if current_type == new_type:
                return []
        else:
            raise AttributeError(
                f"No data type defined for {self.graph.id_label(node_id)}"
            )
        result = self.graph.graph.successors(node_id)
        return [self.graph.get_node(node_id=node_id) for node_id in result]

    def column_predecessors(self, namespace: str, name: str):
        node_id = self.graph.get_node_id(namespace, name)
        predecessors = (
            self.graph.get_node(node_id=node_id)
            for node_id in self.graph.graph.predecessors(node_id)
        )
        col_predecessors = tuple(
            node for node in predecessors if node["grai"]["node_type"] == "Column"
        )
        return col_predecessors

    def test_unique_violations(self, namespace: str, name: str, expects_unique: bool):
        """

        :param namespace:
        :param name:
        :param expects_unique: can't evaluate anything in the case of None
        :return:
        """
        check_downstream, check_upstream = True, True
        node_id = self.graph.get_node_id(namespace, name)
        current_node = self.graph.get_node(node_id=node_id)
        assert (
            current_node.spec.metadata["grai"]["node_type"] == "Column"
        ), "Unique violation tests can only be applied to columns"

        is_unique = (
            current_node.spec.metadata["grai"]
            .get("node_attributes", {})
            .get("is_unique", None)
        )

        if is_unique is None:
            check_upstream = False

        affected_nodes = []
        for node in self.graph.graph.successors(node_id):
            predecessors = self.column_predecessors(node)
            if len(predecessors) == 1:
                # successor is a direct descendant
                test_node_id = predecessors[0]
                test_node = self.graph.get_node(node_id=test_node_id)
                test_is_unique = get_is_unique(test_node)

                if test_is_unique is not None and test_is_unique != expects_unique:
                    affected_nodes.append(test_node)
