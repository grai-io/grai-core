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


@pytest.mark.parametrize("versioned_client", clients)
def test_update_no_updates(versioned_client):
    result = update(versioned_client, [])
    assert result is None


@pytest.mark.parametrize("versioned_client", clients)
def test_update_nodes(versioned_client):
    result = update(versioned_client, TEST_NODES)
    assert result is None


def test_update_node_creation(client):
    nodes = [mock_v1_node() for _ in range(1)]
    namespace = nodes[0].spec.namespace
    update(client, nodes)
    new_nodes = client.get(nodes[0].type, "*", namespace)
    assert len(new_nodes) == len(nodes)


def test_update_node_update(client):
    nodes = [mock_v1_node() for _ in range(1)]
    namespace = nodes[0].spec.namespace
    update(client, nodes)
    new_nodes = client.get(nodes[0].type, "*", namespace)
    assert len(new_nodes) == len(nodes)

    update(client, nodes)
    new_nodes = client.get(nodes[0].type, "*", namespace)
    assert len(new_nodes) == len(nodes)


def test_update_node_deactivate(client):
    nodes = [mock_v1_node() for _ in range(1)]
    namespace = nodes[0].spec.namespace
    update(client, nodes)
    new_nodes = client.get(nodes[0].type, "*", namespace)
    assert len(new_nodes) == len(nodes)
    for node in nodes:
        node.spec.is_active = False
    update(client, nodes)
    new_nodes = client.get(nodes[0].type, "*", namespace)
    assert len(new_nodes) == len(nodes)
    assert all(node.spec.is_active for node in new_nodes)
