import datetime
import uuid
from typing import get_args

import pytest

from grai_client.schemas import edge, node, schema


def make_v1_node():
    return {
        "type": "Node",
        "version": "v1",
        "spec": {
            "id": uuid.uuid4(),
            "name": "test",
            "namespace": "test-ns",
            "data_source": "tests",
            "display_name": "ouch",
            "is_active": True,
            "metadata": {
                "grai": {"node_type": "Node", "node_attributes": {}},
                "test_dict": {"a": "b"},
                "test_list": [1, 2, 3],
                "test_tuple": (4, 5, 6),
                "test_date": datetime.date(2021, 3, 14),
            },
        },
    }


def make_v1_edge():
    return {
        "type": "Edge",
        "version": "v1",
        "spec": {
            "id": uuid.uuid4(),
            "name": "test",
            "namespace": "test2",
            "data_source": "tests",
            "source": {
                "namespace": "sou",
                "name": "rce",
            },
            "destination": {
                "namespace": "desti",
                "name": "nation",
            },
            "is_active": True,
            "metadata": {
                "grai": {"edge_type": "Edge", "edge_attributes": {}},
            },
        },
    }


@pytest.mark.parametrize(
    "test_type,result",
    [
        (node.NodeV1, True),
        (node.NodeTypes, True),
        (edge.EdgeV1, False),
        (edge.EdgeTypes, False),
    ],
)
def test_v1_node_typing(test_type, result):
    obj_dict = make_v1_node()
    obj = schema.Schema(entity=obj_dict)
    assert (
        isinstance(obj.entity, test_type) == result
    ), f"{type(obj)}=={test_type} should be {result}"


@pytest.mark.parametrize(
    "test_type,result",
    [
        (node.NodeV1, False),
        (node.NodeTypes, False),
        (edge.EdgeV1, True),
        (edge.EdgeTypes, True),
    ],
)
def test_v1_edge_typing(test_type, result):
    obj_dict = make_v1_edge()
    obj = schema.Schema(entity=obj_dict)
    assert (
        isinstance(obj.entity, test_type) == result
    ), f"{type(obj)}=={test_type} should be {result}"
