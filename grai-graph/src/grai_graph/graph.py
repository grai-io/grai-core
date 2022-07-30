import uuid
from functools import lru_cache
from typing import Any, Dict, List, Sequence, Tuple, Type, Union

import networkx as nx
from grai_client.schemas.edge import EdgeTypes
from grai_client.schemas.node import NodeTypes
from grai_client.schemas.schema import GraiType, Schema
from multimethod import multimethod


class GraphManifest:
    def __init__(self, nodes: Sequence[NodeTypes], edges: Sequence[EdgeTypes]):
        self.nodes: Sequence[NodeTypes] = nodes
        self.edges: Sequence[EdgeTypes] = edges

        self.node_index: Dict[str, Dict[str, NodeTypes]] = {}
        for node in nodes:
            self.node_index.setdefault(node.spec.namespace, {})
            self.node_index[node.spec.namespace].setdefault(node.spec.name, node)
        # assert all(isinstance(node.spec.id, uuid.UUID) for node in self.nodes), \
        #     "Graph manifests require node UUID's rather than name/namespace specification"
        # assert all(isinstance(edge.spec.source, uuid.UUID) and isinstance(edge.spec.destination, uuid.UUID)
        #            for edge in self.edges), \
        #     "Graph manifests require edge source/destination UUID's rather than name/namespace specification"

    def get_node(self, namespace: str, name: str) -> NodeTypes:
        return self.node_index[namespace][name]


class Graph(nx.DiGraph):
    _container_key = 'obj'

    def __init__(self, manifest):
        self.manifest: GraphManifest = manifest

        super().__init__()
        self.add_nodes_from(self.add_nodes_from_manifest())
        self.add_edges_from(self.add_edges_from_manifest())

    def add_nodes_from_manifest(self):
        return ((hash(node.spec), {self._container_key: node})
                for node in self.manifest.nodes)

    def add_edges_from_manifest(self):
        return ((hash(edge.spec.source), hash(edge.spec.destination), {self._container_key: edge})
                for edge in self.manifest.edges)

    @lru_cache
    def get_node_id(self, namespace: str, name: str) -> int:
        node = self.manifest.get_node(namespace, name)
        return hash(node)

    def get_node(self, namespace: str, name: str) -> GraiType:
        node_id = self.get_node_id(namespace, name)
        return self.nodes.get(node_id)[self._container_key]

    def label(self, namespace: str, name: str) -> str:
        return self.get_node(namespace, name).spec.display_name


@multimethod
def process_items(vals: Any, version: Any, type: Any) -> List[GraiType]:
    raise NotImplementedError()


@process_items.register
def process_dict(dict_item: Dict, version: str, type: str) -> GraiType:
    return Schema.to_model(dict_item, version, type)


@process_items.register
def process_node(item: NodeTypes, version: str, type: str) -> GraiType:
    return item


@process_items.register
def process_edge(item: EdgeTypes, version: str, type: str) -> GraiType:
    return item


@process_items.register
def process_sequence(item_iter: Sequence, version: str, type: str) -> List[GraiType]:
    return [process_items(item, version, type) for item in item_iter]


def build_graph(nodes: List[Dict], edges: List[Dict], version: str) -> Graph:
    nodes = process_items(nodes, version, 'Node')
    edges = process_items(edges, version, 'Edge')
    manifest = GraphManifest(nodes, edges)
    return Graph(manifest)
