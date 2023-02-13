import datetime
import uuid
from typing import get_args

import pytest
from grai_schemas.base import Edge, Node
from grai_schemas.schema import Schema
from grai_schemas.v1 import EdgeV1, NodeV1


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
        (NodeV1, True),
        (Node, True),
        (EdgeV1, False),
        (Edge, False),
    ],
)
def test_v1_node_typing(test_type, result):
    obj_dict = make_v1_node()
    obj = Schema(entity=obj_dict)
    assert isinstance(obj.entity, test_type) == result, f"{type(obj)}=={test_type} should be {result}"


@pytest.mark.parametrize(
    "test_type,result",
    [
        (NodeV1, False),
        (Node, False),
        (EdgeV1, True),
        (Edge, True),
    ],
)
def test_v1_edge_typing(test_type, result):
    obj_dict = make_v1_edge()
    obj = Schema(entity=obj_dict)
    assert isinstance(obj.entity, test_type) == result, f"{type(obj)}=={test_type} should be {result}"
