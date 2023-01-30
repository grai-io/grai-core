import datetime

import pytest

from grai_client.testing.schema import mock_v1_node
from grai_client.update import update
from grai_client.utilities.tests import get_test_client

clients = [get_test_client()]

extra_metadata = {
    "test_nested_dict": {"a": "b"},
    "test_list": [1, 2, 3],
    "test_tuple": (4, 5, 6),
    "test_set": {7, 8, 9},
    "test_date": datetime.date(2021, 3, 14),
}

TEST_NODES = [mock_v1_node(metadata=extra_metadata) for _ in range(2)]


@pytest.mark.parametrize("client", clients)
def test_update_no_updates(client):
    result = update(client, [])
    assert result is None


@pytest.mark.parametrize("client", clients)
def test_update_nodes(client):
    result = update(client, TEST_NODES)
    assert result is None


def test_update_deactivate():
    test_node = get_test_node()
    result = client.get("node", "*", test_node.spec.namespace)
    assert isinstance(result, list)
    assert len(result) == 1  # node namespace is a uuid and therefore unique
    assert result[0].spec.name == test_node.spec.name
    assert result[0].spec.namespace == test_node.spec.namespace
