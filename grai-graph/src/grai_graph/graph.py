import networkx as nx
from typing import List, Type, Any, Tuple, Union, Dict
from grai_graph.schemas import BaseNode, BaseEdge
from functools import singledispatch

NodeTypes = Union[Type[BaseNode], BaseNode]
EdgeTypes = Union[Type[BaseEdge], BaseEdge]


class GraphManifest:
    def __init__(self, nodes, edges):
        self.nodes: List[NodeTypes] = nodes
        self.edges: List[EdgeTypes] = edges


class Graph(nx.DiGraph):
    def __init__(self, manifest):
        self.manifest: GraphManifest = manifest

        super().__init__()
        self.add_nodes_from(self.manifest.nodes)
        self.add_edges_from(self.manifest.edges)

    def downstream_nodes(self, node_id):
        return nx.bfs_successors(self, node_id)


@singledispatch
def process_nodes(node_vals: Any) -> List[NodeTypes]:
    raise NotImplementedError()


@process_nodes.register(List)
@process_nodes.register(Tuple)
def _(node_iter: List) -> List[NodeTypes]:
    return [BaseNode(**node) for node in node_iter]


@process_nodes.register(Dict)
def _(node_dict: Dict) -> NodeTypes:
    return BaseNode(**node_dict)


@singledispatch
def process_edges(edge_vals: Any) -> List[EdgeTypes]:
    raise NotImplementedError()


@process_edges.register(List)
@process_edges.register(Tuple)
def _(edge_iter: List) -> List[EdgeTypes]:
    return [BaseEdge(**node) for node in edge_iter]


@process_edges.register(Dict)
def _(edge_dict: Dict) -> EdgeTypes:
    return BaseEdge(**edge_dict)


def build_graph(nodes: List[Dict], edges: List[Dict]) -> Graph:
    nodes = process_nodes(nodes)
    edges = process_edges(edges)
    manifest = GraphManifest(nodes, edges)
    return Graph(manifest)
