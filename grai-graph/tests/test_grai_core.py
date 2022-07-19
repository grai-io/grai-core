from grai_graph import __version__
from grai_graph import graph
from grai_graph.schemas import BaseNode, BaseEdge
import uuid


def test_version():
    assert __version__ == "0.1.0"


def make_node_dict(id=None, name=None, namespace = 'default', data_source='test'):
    node = {
        'id': uuid.uuid4() if id is None else id,
        'name': str(uuid.uuid4()) if name is None else name,
        'namespace': namespace,
        'data_source': data_source
     }
    return node


def make_edge_dict(source, destination, id=None, data_source='test'):
    edge = {
        'id': uuid.uuid4() if id is None else id,
        'destination': destination,
        'source': source,
        'data_source': data_source
     }
    return edge


def test_make_node():
    node = make_node_dict()
    node = BaseNode(**node)
    assert isinstance(node, BaseNode)


def test_make_edge():
    edge = make_edge_dict({'name': 'test', 'namespace': 'test2'}, uuid.uuid4())
    edge = BaseEdge(**edge)
    assert isinstance(edge, BaseEdge)


def test_build_graph():
    nodes = [make_node_dict() for i in range(4)]
    edges = [make_edge_dict(s['id'], d['id']) for s, d in zip(nodes, nodes[1:])]

    graph.build_graph(nodes, edges)
