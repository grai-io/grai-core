from grai_source_fivetran.loader import FivetranConnector
from grai_source_fivetran.models import Edge, NodeTypes


def test_loader_node_types(app_nodes):
    assert all(isinstance(node, NodeTypes) for node in app_nodes)


def test_loader_edge_types(app_edges):
    assert all(isinstance(edge, Edge) for edge in app_edges)
