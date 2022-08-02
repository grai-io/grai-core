import uuid

import networkx as nx
from grai_client.testing.schema import mock_v1_edge, mock_v1_node, mock_v1_edge_and_nodes

from grai_graph import graph


def get_node_id(node):
    return {'name': node.name, 'namespace': node.namespace}


def test_v1_build_graph():
    edges = []
    nodes = []
    for i in range(4):
        e, n = mock_v1_edge_and_nodes()
        edges.append(e)
        nodes.extend(n)
    G = graph.build_graph(nodes, edges, 'v1')
    assert isinstance(G.graph, nx.DiGraph)
