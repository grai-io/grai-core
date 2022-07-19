import networkx as nx
from typing import List, Type, Any, Tuple, Union, Dict
from grai_graph.schemas import BaseNode, BaseEdge
from functools import singledispatch

NodeTypes = Union[Type[BaseNode], BaseNode]
EdgeTypes = Union[Type[BaseEdge], BaseEdge]


class GraphManifest:
    def __init__(self, nodes: List[Dict], edges: List[Dict]):
        self.nodes: List[NodeTypes] = nodes
        self.edges: List[EdgeTypes] = edges


class Graph(nx.DiGraph):
    def __init__(self, manifest):
        self.manifest: GraphManifest = manifest

        super().__init__()
        self.add_nodes_from(self.add_nodes_from_manifest())
        self.add_edges_from(self.add_edges_from_manifest())

    def add_nodes_from_manifest(self):
        return ((node.id, node.dict) for node in self.manifest.nodes)

    def add_edges_from_manifest(self):
        return ((edges.id, edges.dict) for edges in self.manifest.edges)

    def downstream_nodes(self, node_id):
        return nx.bfs_successors(self, node_id)


@singledispatch
def process_nodes(node_vals: Any) -> List[NodeTypes]:
    raise NotImplementedError()


@process_nodes.register(list)
@process_nodes.register(tuple)
def _(node_iter: Union[list, tuple]) -> List[NodeTypes]:
    return [BaseNode(**node) for node in node_iter]


@process_nodes.register
def _(node_dict: dict) -> NodeTypes:
    return BaseNode(**node_dict)


@singledispatch
def process_edges(edge_vals: Any) -> List[EdgeTypes]:
    raise NotImplementedError()


@process_edges.register(list)
@process_edges.register(tuple)
def _(edge_iter: Union[list, tuple]) -> List[EdgeTypes]:
    return [BaseEdge(**edge) for edge in edge_iter]


@process_edges.register
def _(edge_dict: dict) -> EdgeTypes:
    return BaseEdge(**edge_dict)


def build_graph(nodes: List[Dict], edges: List[Dict]) -> Graph:
    nodes = process_nodes(nodes)
    edges = process_edges(edges)
    manifest = GraphManifest(nodes, edges)
    return Graph(manifest)
