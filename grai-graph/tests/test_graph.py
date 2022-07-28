import uuid

from grai_graph import __version__, graph
from grai_client.testing.schema import mock_v1_node, mock_v1_edge


def test_version():
    assert __version__ == "0.1.0"


def test_v1_build_graph():
    nodes = [mock_v1_node()for i in range(4)]
    edges = [mock_v1_edge(source=s.spec.id, destination=d.spec.id) for s, d in zip(nodes, nodes[1:])]

    graph.build_graph(nodes, edges, 'v1')