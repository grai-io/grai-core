from typing import Generator, List, Optional, Tuple

import networkx as nx
from grai_schemas.base import Node as NodeTypes

from grai_graph.graph import Graph


class GraphAnalyzer:
    """ """

    def __init__(self, graph: Graph):
        self.graph = graph

    def downstream_nodes(self, namespace: str, name: str):
        """

        Args:
            namespace (str):
            name (str):

        Returns:

        Raises:

        """
        node_id = self.graph.get_node_id(namespace, name)
        downstream = list(nx.bfs_successors(self.graph.graph, node_id))[0][1]
        return [self.graph.get_node(node_id=node) for node in downstream]

    def upstream_nodes(self, namespace: str, name: str):
        """

        Args:
            namespace (str):
            name (str):

        Returns:

        Raises:

        """
        node_id = self.graph.get_node_id(namespace, name)
        upstream = list(nx.bfs_predecessors(self.graph.graph, node_id))[0][1]
        return [self.graph.get_node(node_id=node) for node in upstream]

    def test_delete_node(self, namespace: str, name: str):
        """

        Args:
            namespace (str):
            name (str):

        Returns:

        Raises:

        """
        return list(self.downstream_nodes(namespace, name))

    def traverse_data_type_violations(
        self, node: NodeTypes, new_type: str, path: Optional[List] = None
    ) -> Generator[Tuple[List[NodeTypes], bool], None, None]:
        """

        Args:
            node (NodeTypes):
            new_type (str):
            path (Optional[List], optional): (Default value = None)

        Returns:

        Raises:

        """
        if path is None:
            path = [node]

        node_id = self.graph.get_node_id(node.spec.namespace, node.spec.name)
        for test_node in self.column_successors(node.spec.namespace, node.spec.name):
            test_node_id = self.graph.get_node_id(test_node.spec.namespace, test_node.spec.name)
            edge_data = self.graph.graph[node_id][test_node_id][self.graph._container_key]

            edge_meta = edge_data.spec.metadata.grai
            node_meta = test_node.spec.metadata.grai

            # TODO What if we don't have information about the edge but both nodes have identical expectations for unique?
            if (
                hasattr(edge_meta.edge_attributes, "preserves_data_type")
                and not edge_meta.edge_attributes.preserves_data_type
            ):
                continue

            new_path = [*path, test_node]

            test_node_data_type = node_meta.node_attributes.data_type
            if test_node_data_type is not None:
                yield (new_path, test_node_data_type == new_type)

            yield from self.traverse_data_type_violations(test_node, new_type, path=new_path)

    def test_data_type_change(self, namespace: str, name: str, new_type: bool) -> List[Tuple[List[NodeTypes], bool]]:
        """

        Args:
            namespace (str):
            name (str):
            new_type (bool):

        Returns:

        Raises:

        """
        node_id = self.graph.get_node_id(namespace, name)

        if node_id is None:
            return []

        current_node = self.graph.get_node(node_id=node_id)
        assert (
            current_node.spec.metadata.grai.node_type == "Column"
        ), f"Data type violation tests can only be applied to columns {current_node.spec.metadata.grai.node_type}"

        # Only looks downstream
        affected_nodes = self.traverse_data_type_violations(current_node, new_type)
        return list(affected_nodes)

    def traverse_unique_violations(
        self, node: NodeTypes, expects_unique: bool, path: Optional[List] = None
    ) -> Generator[Tuple[List[NodeTypes], bool], None, None]:
        """

        Args:
            node (NodeTypes):
            expects_unique (bool):
            path (Optional[List], optional): (Default value = None)

        Returns:

        Raises:

        """
        if path is None:
            path = [node]

        node_id = self.graph.get_node_id(node.spec.namespace, node.spec.name)
        for test_node in self.column_successors(node.spec.namespace, node.spec.name):
            test_node_id = self.graph.get_node_id(test_node.spec.namespace, test_node.spec.name)
            edge_data = self.graph.graph[node_id][test_node_id][self.graph._container_key]
            edge_meta = edge_data.spec.metadata.grai
            node_meta = test_node.spec.metadata.grai

            # TODO What if we don't have information about the edge but both nodes have identical expectations for unique?

            if (
                hasattr(edge_meta.edge_attributes, "preserves_unique")
                and not edge_meta.edge_attributes.preserves_unique
            ):
                continue

            test_node_is_unique = node_meta.node_attributes.is_unique
            new_path = [*path, test_node]

            if test_node_is_unique is not None:
                yield (new_path, test_node_is_unique == expects_unique)

            yield from self.traverse_unique_violations(test_node, expects_unique, path=new_path)

    def test_unique_violations(
        self, namespace: str, name: str, expects_unique: bool
    ) -> List[Tuple[List[NodeTypes], bool]]:
        """

        Args:
            namespace (str):
            name (str):
            expects_unique (bool): can't evaluate anything in the case of None

        Returns:

        Raises:

        """
        node_id = self.graph.get_node_id(namespace, name)

        if node_id is None:
            return []

        current_node = self.graph.get_node(node_id=node_id)
        assert (
            current_node.spec.metadata.grai.node_type == "Column"
        ), f"Unique violation tests can only be applied to columns {current_node.spec.metadata.grai.node_type}"

        # Only looks downstream
        affected_nodes = self.traverse_unique_violations(current_node, expects_unique)
        return list(affected_nodes)

    def traverse_null_violations(
        self, node: NodeTypes, is_nullable: bool, path: Optional[List] = None
    ) -> Generator[Tuple[List[NodeTypes], bool], None, None]:
        """

        Args:
            node (NodeTypes):
            is_nullable (bool):
            path (Optional[List], optional): (Default value = None)

        Returns:

        Raises:

        """
        if path is None:
            path = [node]

        node_id = self.graph.get_node_id(node.spec.namespace, node.spec.name)
        for test_node in self.column_successors(node.spec.namespace, node.spec.name):
            test_node_id = self.graph.get_node_id(test_node.spec.namespace, test_node.spec.name)
            edge_data = self.graph.graph[node_id][test_node_id][self.graph._container_key]

            edge_meta = edge_data.spec.metadata.grai
            node_meta = test_node.spec.metadata.grai

            # TODO What if we don't have information about the edge but both nodes have identical expectations for unique?
            if (
                hasattr(edge_meta.edge_attributes, "preserves_nullable")
                and not edge_meta.edge_attributes.preserves_nullable
            ):
                continue

            new_path = [*path, test_node]

            test_node_is_nullable = node_meta.node_attributes.is_nullable

            if test_node_is_nullable is not None:
                yield (new_path, test_node_is_nullable == is_nullable)

            yield from self.traverse_null_violations(test_node, is_nullable, path=new_path)

    def test_nullable_violations(
        self, namespace: str, name: str, is_nullable: bool
    ) -> List[Tuple[List[NodeTypes], bool]]:
        """

        Args:
            namespace (str):
            name (str):
            is_nullable (bool): can't evaluate anything in the case of None

        Returns:

        Raises:

        """
        node_id = self.graph.get_node_id(namespace, name)

        if node_id is None:
            return []

        current_node = self.graph.get_node(node_id=node_id)
        assert (
            current_node.spec.metadata.grai.node_type == "Column"
        ), f"Unique violation tests can only be applied to columns {current_node.spec.metadata.grai.node_type}"

        # Only looks downstream
        affected_nodes = self.traverse_null_violations(current_node, is_nullable)

        return list(affected_nodes)

    def column_predecessors(self, namespace: str, name: str):
        """

        Args:
            namespace (str):
            name (str):

        Returns:

        Raises:

        """
        node_id = self.graph.get_node_id(namespace, name)
        predecessors = (self.graph.get_node(node_id=node_id) for node_id in self.graph.graph.predecessors(node_id))
        col_predecessors = tuple(node for node in predecessors if node.spec.metadata.grai.node_type == "Column")
        return col_predecessors

    def column_successors(self, namespace: str, name: str):
        """

        Args:
            namespace (str):
            name (str):

        Returns:

        Raises:

        """
        node_id = self.graph.get_node_id(namespace, name)
        successors = (self.graph.get_node(node_id=node_id) for node_id in self.graph.graph.successors(node_id))
        col_successors = tuple(node for node in successors if node.spec.metadata.grai.node_type == "Column")
        return col_successors
