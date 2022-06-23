from grai_graph import __version__
from grai_graph import graph


def test_version():
    assert __version__ == "0.1.0"


def test_build_graph():
    nodes = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3)]
    graph.build_graph(nodes, edges)
