import datetime
import uuid

import pytest
from grai_schemas.v1.mock import MockV1

from grai_client.update import update


@pytest.fixture(scope="module")
def update_sources(client):
    sources = [MockV1.source.source() for _ in range(3)]
    return client.post(sources)


def test_update_node_creation(client, update_sources):
    namespace = str(uuid.uuid4())
    nodes = [MockV1.node.sourced_node(namespace=namespace, data_source=update_sources[0].spec) for _ in range(3)]
    update(client, nodes)

    new_nodes = client.get(nodes[0].type, update_sources[0].spec.id, namespace=namespace)
    assert len(new_nodes) == len(nodes), "update did not create nodes"


def test_update_is_idempotent(client, update_sources):
    namespace = str(uuid.uuid4())
    nodes = [MockV1.node.sourced_node(namespace=namespace, data_source=update_sources[0].spec) for _ in range(3)]
    breakpoint()
    update(client, nodes)
    updated_nodes_1 = client.get(nodes[0].type, update_sources[0].spec.id, namespace=namespace)
    assert len(updated_nodes_1) == len(nodes)
    assert all(node1.spec.metadata == node2.spec.metadata for node1, node2 in zip(updated_nodes_1, nodes))

    update(client, nodes)
    updated_nodes_2 = client.get(nodes[0].type, update_sources[0].spec.id, namespace=namespace)
    assert len(updated_nodes_2) == len(nodes)
    assert all(node1 == node2 for node1, node2 in zip(updated_nodes_1, updated_nodes_2)), "update is not idempotent"


def test_update_node_patched(client, update_sources):
    namespace = str(uuid.uuid4())
    nodes = [MockV1.node.sourced_node(namespace=namespace, data_source=update_sources[0].spec) for _ in range(3)]
    new_nodes = client.post(nodes)
    for node in new_nodes:
        node.spec.metadata.grai.node_attributes.patched = True

    update(client, new_nodes)
    new_nodes = client.get(nodes[0].type, update_sources[0].spec.id, namespace=namespace)

    assert len(new_nodes) == len(nodes), "Update altered the number of nodes"
    assert all(
        getattr(node.spec.metadata.grai.node_attributes, "patched", False) for node in new_nodes
    ), "Update did not patch nodes"
    assert all(
        node.spec.metadata.grai.node_attributes.patched is True for node in new_nodes
    ), "Update did not patch nodes correctly"


# TODO: This is known to fail because the update function does not currently support deactivating nodes
def test_update_node_deletes(client, update_sources):
    namespace = str(uuid.uuid4())
    nodes = [MockV1.node.sourced_node(namespace=namespace, data_source=update_sources[0].spec) for _ in range(3)]
    new_nodes = client.post(nodes)

    assert len(new_nodes) == len(nodes)

    updated_nodes = [new_nodes[0]]
    update(client, updated_nodes)
    remaining_nodes = client.get(nodes[0].type, update_sources[0].spec.id, namespace=namespace)
    assert len(remaining_nodes) == len(updated_nodes)
