import uuid
import pytest

from grai_client.schemas import edge, node, schema


def make_v1_node():
    return {
        'type': "Node",
        'version': 'v1',
        'spec': {
            'id': uuid.uuid4(),
            'name': "test",
            'namespace': "test-ns",
            'data_source': 'tests',
            'display_name': 'ouch',
            'is_active': True,
            'metadata': {}
        },
    }


def make_v1_edge():
    return {
        'type': "Edge",
        'version': 'v1',
        'spec': {
            'id': uuid.uuid4(),
            'data_source': 'tests',
            'source': uuid.uuid4(),
            'destination': uuid.uuid4(),
            'is_active': True,
            'metadata': {}
        },
    }


@pytest.mark.parametrize('type,result', [
    (node.NodeV1, True),
    (node.NodeTypes, True),
    (edge.EdgeV1, False),
    (edge.EdgeTypes, False)
])
def test_v1_node_typing(type, result):
    obj_dict = make_v1_node()
    obj = schema.Schema(entity=obj_dict)
    assert isinstance(obj.entity, type) == result


@pytest.mark.parametrize('type,result', [
    (node.NodeV1, False),
    (node.NodeTypes, False),
    (edge.EdgeV1, True),
    (edge.EdgeTypes, True)
])
def test_v1_edge_typing(type, result):
    obj_dict = make_v1_edge()
    obj = schema.Schema(entity=obj_dict)
    assert isinstance(obj.entity, type) == result
