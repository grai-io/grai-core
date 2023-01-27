from functools import lru_cache
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, Union

import networkx as nx
from grai_schemas.base import Edge as EdgeTypes
from grai_schemas.base import Node as NodeTypes
from grai_schemas.schema import GraiType, Schema
from multimethod import multimethod


class GraphManifest:
    def __init__(self, nodes: Sequence[NodeTypes], edges: Sequence[EdgeTypes]):
        self.nodes: Sequence[NodeTypes] = nodes
        self.edges: Sequence[EdgeTypes] = edges

        self.node_index: Dict[str, Dict[str, NodeTypes]] = {}
        for node in nodes:
            self.node_index.setdefault(node.spec.namespace, {})
            self.node_index[node.spec.namespace].setdefault(node.spec.name, node)

    def get_node(self, namespace: str, name: str) -> Optional[NodeTypes]:
        return self.node_index.get(namespace, {}).get(name, None)


class Graph:
    _container_key = "obj"

    def __init__(self, manifest):
        self.manifest: GraphManifest = manifest
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(self.add_nodes_from_manifest())
        self.graph.add_edges_from(self.add_edges_from_manifest())

    def add_nodes_from_manifest(self):
        return ((hash(node.spec), {self._container_key: node}) for node in self.manifest.nodes)

    def add_edges_from_manifest(self):
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
        node = self.manifest.get_node(namespace, name)
        return hash(node.spec) if node is not None else node

    def get_node(
        self,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        node_id: Optional[int] = None,
    ) -> GraiType:
        if namespace and name:
            node_id = self.get_node_id(namespace, name)
            if node_id is None:
                raise Exception(f"No nodes found with name={name} and namespace={namespace}")
        elif not node_id:
            raise Exception(f"`get_node` requires either name & namespace or node_id argument")

        return self.graph.nodes.get(node_id)[self._container_key]

    def label(self, namespace: str, name: str) -> str:
        return self.get_node(namespace, name).spec.display_name

    def id_label(self, node_id: int) -> str:
        return self.get_node(node_id=node_id).spec.display_name

    def relabeled_graph(self):
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
    message = f"Process items does not have an implementation for " f"{vals=}, {version=}, {type=}"
    raise NotImplementedError(message)


@process_items.register
def process_dict(dict_item: Dict, version: str, type: str) -> GraiType:
    return Schema.to_model(dict_item, version, type)


@process_items.register
def process_node(item: GraiType, version: str, type: str) -> GraiType:
    return item


@process_items.register
def process_sequence(item_iter: Sequence, version: str, type: str) -> List[GraiType]:
    return [process_items(item, version, type) for item in item_iter]


def build_graph(nodes: List[Dict], edges: List[Dict], version: str) -> Graph:
    nodes = process_items(nodes, version, "Node")
    edges = process_items(edges, version, "Edge")
    manifest = GraphManifest(nodes, edges)

    return Graph(manifest)
