from collections import Counter, defaultdict
from functools import cached_property, lru_cache
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Type, Union
from uuid import UUID

import networkx as nx
from grai_schemas.base import Edge as EdgeTypes
from grai_schemas.base import Node as NodeTypes
from grai_schemas.schema import GraiType, Schema
from multimethod import multimethod


class GraphManifest:
    """ """

    def __init__(self, nodes: Sequence[NodeTypes], edges: Sequence[EdgeTypes]):
        self.nodes: Sequence[NodeTypes] = nodes
        self.edges: Sequence[EdgeTypes] = edges

        self.node_index: Dict[str, Dict[str, NodeTypes]] = {}
        for node in nodes:
            self.node_index.setdefault(node.spec.namespace, {})
            self.node_index[node.spec.namespace].setdefault(node.spec.name, node)

    def get_node(self, namespace: str, name: str) -> Optional[NodeTypes]:
        """

        Args:
            namespace (str):
            name (str):

        Returns:

        Raises:

        """
        return self.node_index.get(namespace, {}).get(name, None)


class Graph:
    """ """

    _container_key = "obj"

    def __init__(self, manifest):
        self.manifest: GraphManifest = manifest
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(self.add_nodes_from_manifest())
        self.graph.add_edges_from(self.add_edges_from_manifest())

    def add_nodes_from_manifest(self):
        """ """
        return ((hash(node.spec), {self._container_key: node}) for node in self.manifest.nodes)

    def add_edges_from_manifest(self):
        """ """
        return (
            (
                hash(edge.spec.source),
                hash(edge.spec.destination),
                {self._container_key: edge},
            )
            for edge in self.manifest.edges
        )

    @lru_cache
    def get_node_id(self, namespace: str, name: str) -> Optional[int]:
        """

        Args:
            namespace (str):
            name (str):

        Returns:

        Raises:

        """
        node = self.manifest.get_node(namespace, name)
        return hash(node.spec) if node is not None else node

    def get_node(
        self,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        node_id: Optional[int] = None,
    ) -> GraiType:
        """

        Args:
            namespace (Optional[str], optional): (Default value = None)
            name (Optional[str], optional): (Default value = None)
            node_id (Optional[int], optional): (Default value = None)

        Returns:

        Raises:

        """
        if namespace and name:
            node_id = self.get_node_id(namespace, name)
            if node_id is None:
                raise Exception(f"No nodes found with name={name} and namespace={namespace}")
        elif not node_id:
            raise Exception(f"`get_node` requires either name & namespace or node_id argument")

        return self.graph.nodes.get(node_id)[self._container_key]

    def label(self, namespace: str, name: str) -> str:
        """

        Args:
            namespace (str):
            name (str):

        Returns:

        Raises:

        """
        return self.get_node(namespace, name).spec.display_name

    def id_label(self, node_id: int) -> str:
        """

        Args:
            node_id (int):

        Returns:

        Raises:

        """
        return self.get_node(node_id=node_id).spec.display_name

    def relabeled_graph(self):
        """ """
        label_map = {hash(node.spec): f"{node.spec.namespace}-{node.spec.name}" for node in self.manifest.nodes}
        nodes = label_map.values()
        edges = (
            (
                hash(edge.spec.source),
                hash(edge.spec.destination),
                {self._container_key: edge},
            )
            for edge in self.manifest.edges
        )
        edges = ((label_map[edge[0]], label_map[edge[1]], {}) for edge in edges)
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        return graph


@multimethod
def process_items(vals: Any, version: Any, type: Any) -> List[GraiType]:
    """

    Args:
        vals (Any):
        version (Any):
        type (Any):

    Returns:

    Raises:

    """
    message = f"Process items does not have an implementation for " f"{vals=}, {version=}, {type=}"
    raise NotImplementedError(message)


@process_items.register
def process_dict(dict_item: Dict, version: str, type: str) -> GraiType:
    """

    Args:
        dict_item (Dict):
        version (str):
        type (str):

    Returns:

    Raises:

    """
    return Schema.to_model(dict_item, version, type)


@process_items.register
def process_node(item: GraiType, version: str, type: str) -> GraiType:
    """

    Args:
        item (GraiType):
        version (str):
        type (str):

    Returns:

    Raises:

    """
    return item


@process_items.register
def process_sequence(item_iter: Sequence, version: str, type: str) -> List[GraiType]:
    """

    Args:
        item_iter (Sequence):
        version (str):
        type (str):

    Returns:

    Raises:

    """
    return [process_items(item, version, type) for item in item_iter]


def build_graph(nodes: List[Dict], edges: List[Dict], version: str) -> Graph:
    """

    Args:
        nodes (List[Dict]):
        edges (List[Dict]):
        version (str):

    Returns:

    Raises:

    """

    nodes = process_items(nodes, version, "Node")
    edges = process_items(edges, version, "Edge")
    manifest = GraphManifest(nodes, edges)

    return Graph(manifest)


class BaseSourceSegment:
    def __init__(self, node_source_map: Dict[UUID, Iterable], edge_map: Dict[UUID, UUID]):
        self.node_source_map = {k: frozenset(v) for k, v in node_source_map.items()}
        self.edge_map = edge_map

    @cached_property
    def covering_set(self) -> tuple:
        # I think removing repeated sets won't affect the minimal covering set computation 🤞
        sets = set(self.node_source_map.values())

        result = []
        while sets:
            frequency = Counter(elem for s in sets for elem in s)
            max_element = max(frequency, key=frequency.get)
            result.append(max_element)
            sets = [s for s in sets if max_element not in s]

        return tuple(result)

    @cached_property
    def node_cover_map(self) -> dict:
        result: dict = {}
        for key, source_set in self.node_source_map.items():
            for cover in self.covering_set:
                if cover in source_set:
                    result[key] = cover
                    break
        return result

    @cached_property
    def cover_edge_map(self) -> Dict[str, List[str]]:
        result = defaultdict(set)
        for source, destination in self.edge_map.items():
            source_cover = self.node_cover_map[source]
            destination_cover = self.node_cover_map[destination]
            result[source_cover].add(destination_cover)
        return {k: list(v) for k, v in result.items()}


class SourceSegment(BaseSourceSegment):
    def __init__(self, nodes: List[NodeTypes], edges: List[EdgeTypes]):
        # Assumes we are providing SourceSpecs not UUIDs in data_sources
        node_source_map = {node.spec.id: frozenset(source.name for source in node.spec.data_sources) for node in nodes}
        if None in node_source_map:
            raise ValueError("All values in `nodes` must be of NodeType and their `.spec.id` value must not be empty.")

        edge_map = {}
        for edge in edges:
            source = edge.spec.source.id if not isinstance(edge.spec.source, UUID) else edge.spec.source
            destination = (
                edge.spec.destination.id if not isinstance(edge.spec.destination, UUID) else edge.spec.destination
            )
            edge_map[source] = destination

        if None in edge_map:
            raise ValueError(
                "All values in `edges` must be of EdgeType and both `.spec.source.id` and `.spec.destination.id` "
                "values must not be empty."
            )
        super().__init__(node_source_map=node_source_map, edge_map=edge_map)
