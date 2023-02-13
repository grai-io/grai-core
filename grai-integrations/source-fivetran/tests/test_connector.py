from grai_source_fivetran.loader import FivetranGraiMapper
from grai_source_fivetran.models import Edge, NodeTypes


def test_loader_node_types(nodes):
    assert all(isinstance(node, NodeTypes) for node in nodes)


def test_loader_edge_types(edges):
    assert all(isinstance(edge, Edge) for edge in edges)
