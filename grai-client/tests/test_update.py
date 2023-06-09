import datetime
import uuid

import pytest

from grai_client.testing.schema import mock_v1_node
from grai_client.update import update


def test_update_node_creation(client):
    namespace = str(uuid.uuid4())
    nodes = [mock_v1_node(namespace=namespace) for _ in range(3)]
    update(client, nodes)
    new_nodes = client.get(nodes[0].type, namespace=namespace)
    assert len(new_nodes) == len(nodes), "update did not create nodes"


def test_update_is_idempotent(client):
    namespace = str(uuid.uuid4())
    nodes = [mock_v1_node(namespace=namespace) for _ in range(3)]
    update(client, nodes)
    updated_nodes_1 = client.get(nodes[0].type, namespace=namespace)
    assert len(updated_nodes_1) == len(nodes)

    update(client, nodes)
    updated_nodes_2 = client.get(nodes[0].type, namespace=namespace)
    assert len(updated_nodes_2) == len(nodes)
    assert all(node1 == node2 for node1, node2 in zip(updated_nodes_1, updated_nodes_2)), "update is not idempotent"


def test_update_node_patched(client):
    namespace = str(uuid.uuid4())
    nodes = [mock_v1_node(namespace=namespace) for _ in range(3)]

    new_nodes = client.post(nodes)
    for node in new_nodes:
        node.spec.metadata.grai.node_attributes["patched"] = True

    update(client, new_nodes)
    new_nodes = client.get(nodes[0].type, namespace=namespace)

    assert len(new_nodes) == len(nodes), "Update altered the number of nodes"
    assert all(
        node.spec.metadata.grai.node_attributes.get("patched", False) for node in new_nodes
    ), "Update did not patch nodes"
    assert all(
        node.spec.metadata.grai.node_attributes["patched"] is True for node in new_nodes
    ), "Update did not patch nodes correctly"


# TODO: This is known to fail because the update function does not currently support deactivating nodes
# def test_update_node_deactivate(client):
#     nodes = [mock_v1_node() for _ in range(1)]
#     namespace = nodes[0].spec.namespace
#     update(client, nodes)
#     new_nodes = client.get(nodes[0].type, namespace=namespace)
#     assert len(new_nodes) == len(nodes)
#     for node in nodes:
#         node.spec.is_active = False
#     update(client, nodes)
#     new_nodes = client.get(nodes[0].type, namespace=namespace)
#     assert len(new_nodes) == len(nodes)
#     assert all(node.spec.is_active is False for node in new_nodes)
