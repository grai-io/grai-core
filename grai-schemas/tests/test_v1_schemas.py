import datetime
import uuid
from typing import get_args

import pytest
from grai_schemas.base import Edge, Node
from grai_schemas.schema import Schema
from grai_schemas.v1 import EdgeV1, NodeV1


def extra_metadata():
    return {
        "test_dict": {"a": "b"},
        "test_list": [1, 2, 3],
        "test_tuple": (4, 5, 6),
        "test_date": datetime.date(2021, 3, 14),
    }


def make_v1_node():
    """ """
    node = {
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
                "grai": {"node_type": "Generic", "node_attributes": {}, "tags": ["pii", "phi"]},
                **extra_metadata(),
            },
        },
    }
    return {**node}


def make_v1_edge():
    """ """
    edge = {
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
                "grai": {"edge_type": "Generic", "edge_attributes": {}, "tags": ["pii", "phi"]},
                **extra_metadata(),
            },
        },
    }
    return {**edge}


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
    """

    Args:
        test_type:
        result:

    Returns:

    Raises:

    """
    obj_dict = make_v1_edge()
    obj = Schema(entity=obj_dict)
    assert isinstance(obj.entity, test_type) == result, f"{type(obj)}=={test_type} should be {result}"


# test adding a new field to the metadata of a node
def test_adding_new_field_to_node_metadata():
    """ """
    obj_dict = make_v1_node()
    obj = Schema(entity=obj_dict)
    obj.entity.spec.metadata.new_field = "new_value"
    assert obj.entity.spec.metadata.new_field == "new_value"


def test_adding_new_field_to_edge_metadata():
    """ """
    obj_dict = make_v1_edge()
    obj = Schema(entity=obj_dict)
    obj.entity.spec.metadata.new_field = "new_value"
    assert obj.entity.spec.metadata.new_field == "new_value"


def test_node_from_spec_no_metadata():
    """ """

    obj_dict = make_v1_node()["spec"]
    obj_dict.pop("metadata")
    obj = NodeV1.from_spec(obj_dict)
    assert isinstance(obj, NodeV1)
    assert hasattr(obj.spec, "metadata")
    assert hasattr(obj.spec.metadata, "grai")


def test_edge_from_spec_no_metadata():
    """ """
    obj_dict = make_v1_edge()["spec"]
    obj_dict.pop("metadata")
    obj = EdgeV1.from_spec(obj_dict)
    assert isinstance(obj, EdgeV1)
    assert hasattr(obj.spec, "metadata")
    assert hasattr(obj.spec.metadata, "grai")


def test_edge_from_spec_no_grai_metadata():
    """ """
    obj_dict = make_v1_edge()["spec"]
    obj_dict["metadata"].pop("grai")
    obj = EdgeV1.from_spec(obj_dict)
    assert isinstance(obj, EdgeV1)
    assert hasattr(obj.spec, "metadata")
    assert hasattr(obj.spec.metadata, "grai")


def test_node_from_spec_no_grai_metadata():
    """ """
    obj_dict = make_v1_node()["spec"]
    obj_dict["metadata"].pop("grai")
    obj_dict["metadata"]["test_values"] = (1, 2, 3)
    obj = NodeV1.from_spec(obj_dict)
    assert isinstance(obj, NodeV1)
    assert hasattr(obj.spec, "metadata")
    assert hasattr(obj.spec.metadata, "grai")
    obj_dict["metadata"]["test_values"] = (1, 2, 3)


def test_node_from_spec_preserves_extra():
    obj_dict = make_v1_node()["spec"]
    obj_dict["metadata"]["test_values"] = (1, 2, 3)
    obj = NodeV1.from_spec(obj_dict)
    assert hasattr(obj.spec.metadata, "test_values")
    assert obj.spec.metadata.test_values == (1, 2, 3)


def test_edge_from_spec_preserves_extra():
    obj_dict = make_v1_edge()["spec"]
    obj_dict["metadata"]["test_values"] = (1, 2, 3)
    obj = EdgeV1.from_spec(obj_dict)
    assert hasattr(obj.spec.metadata, "test_values")
    assert obj.spec.metadata.test_values == (1, 2, 3)
