import datetime
import uuid
from typing import get_args

import pytest
from grai_schemas.base import Edge, Node
from grai_schemas.schema import Schema
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.mock import MockV1

mocker = MockV1()


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
    """

    Args:
        test_type:
        result:

    Returns:

    Raises:

    """
    obj_dict = mocker.node_dict()
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
    """

    Args:
        test_type:
        result:

    Returns:

    Raises:

    """
    obj_dict = mocker.edge_dict()
    obj = Schema(entity=obj_dict)
    assert isinstance(obj.entity, test_type) == result, f"{type(obj)}=={test_type} should be {result}"


# test adding a new field to the metadata of a node
def test_adding_new_field_to_metadata():
    """ """
    node_dict = mocker.node_dict()
    obj = Schema(entity=node_dict)
    obj.entity.spec.metadata["new_field"] = "new_value"
    assert obj.entity.spec.metadata["new_field"] == "new_value"
