import datetime
import uuid

import pytest

from grai_client.schemas import edge, node, schema
from grai_client.update import update
from grai_client.utilities.tests import get_test_client

clients = [get_test_client()]


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
                "test_nested_dict": {"a": "b"},
                "test_list": [1, 2, 3],
                "test_tuple": (4, 5, 6),
                "test_set": {7, 8, 9},
                "test_date": datetime.date(2021, 3, 14),
            },
        },
    }


TEST_NODES = [schema.Schema(entity=make_v1_node()).entity for _ in range(2)]


@pytest.mark.parametrize("client", clients)
def test_update_no_updates(client):
    result = update(client, [])
    assert result is None


@pytest.mark.parametrize("client", clients)
def test_update_nodes(client):
    result = update(client, TEST_NODES)
    assert result is None
