import uuid

from grai_client.testing.schema import mock_v1_edge, mock_v1_node

from grai_graph import __version__, graph


def test_version():
    assert __version__ == "0.1.0"

def get_node_id(node):
    return {'name': node.name, 'namespace': node.namespace}

def test_v1_build_graph():
    nodes = [mock_v1_node()for i in range(4)]
    edges = [mock_v1_edge(source=get_node_id(s.spec), destination=get_node_id(d.spec)) for s, d in zip(nodes, nodes[1:])]

    graph.build_graph(nodes, edges, 'v1')