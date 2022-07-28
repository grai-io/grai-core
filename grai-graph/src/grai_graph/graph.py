from functools import cache
from typing import Any, Dict, List, Tuple, Type, Union, Sequence

import networkx as nx
from grai_client.schemas.schema import GraiType, Schema
from grai_client.schemas.node import NodeTypes
from grai_client.schemas.edge import EdgeTypes
from multimethod import multimethod
import uuid


class GraphManifest:
    def __init__(self, nodes: Sequence[NodeTypes], edges: Sequence[EdgeTypes]):
        self.nodes: Sequence[NodeTypes] = nodes
        self.edges: Sequence[EdgeTypes] = edges
        assert all(isinstance(node.spec.id, uuid.UUID) for node in self.nodes), \
            "Graph manifests require node UUID's rather than name/namespace specification"
        assert all(isinstance(edge.spec.source, uuid.UUID) and isinstance(edge.spec.destination, uuid.UUID)
                   for edge in self.edges), \
            "Graph manifests require edge source/destination UUID's rather than name/namespace specification"


class Graph(nx.DiGraph):
    def __init__(self, manifest):
        self.manifest: GraphManifest = manifest

        super().__init__()
        self.add_nodes_from(self.add_nodes_from_manifest())
        self.add_edges_from(self.add_edges_from_manifest())

    def add_nodes_from_manifest(self):
        return ((node.spec.id, node.dict()) for node in self.manifest.nodes)

    def add_edges_from_manifest(self):
        return ((edge.spec.source, edge.spec.destination, edge.dict()) for edge in self.manifest.edges)

    def downstream_nodes(self, node_id):
        return nx.bfs_successors(self, node_id)

    @cache
    def label(self, node_id: Union[str, uuid.UUID]) -> str:
        if isinstance(node_id, str):
            node_id = uuid.UUID(node_id)
        return self.nodes.get(node_id)['spec']['display_name']


@multimethod
def process_items(vals: Any, version: Any, type: Any) -> List[GraiType]:
    raise NotImplementedError()


@process_items.register
def _(dict_item: Dict, version: str, type: str) -> GraiType:
    return Schema.to_model(dict_item, version, type)


@process_items.register
def _(item: NodeTypes, version: str, type: str) -> GraiType:
    return item


@process_items.register
def _(item: EdgeTypes, version: str, type: str) -> GraiType:
    return item


@process_items.register
def _(item_iter: Sequence, version: str, type: str) -> List[GraiType]:
    return [process_items(item, version, type) for item in item_iter]


def build_graph(nodes: List[Dict], edges: List[Dict], version: str) -> Graph:
    nodes = process_items(nodes, version, 'Node')
    edges = process_items(edges, version, 'Edge')
    manifest = GraphManifest(nodes, edges)
    return Graph(manifest)
