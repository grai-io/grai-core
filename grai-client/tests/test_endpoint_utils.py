import datetime
import uuid
from typing import get_args

from grai_client.endpoints.utilities import serialize_obj


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
                "test_dict": {"a": "b"},
                "test_list": [1, 2, 3],
                "test_tuple": (4, 5, 6),
                "test_date": datetime.date(2021, 3, 14),
            },
        },
    }


def test_serialize_obj():
    obj = make_v1_node()
    json = serialize_obj(obj)
    assert isinstance(json, (str, bytes)), type(json)
