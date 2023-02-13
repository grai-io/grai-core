from functools import cache

import pytest
from grai_schemas.v1 import EdgeV1, NodeV1
from requests import RequestException

from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.schema import Schema
from grai_client.testing.schema import (
    mock_v1_edge,
    mock_v1_edge_and_nodes,
    mock_v1_node,
)
from grai_client.utilities.tests import get_test_client

client = get_test_client()


@cache
def get_test_node():
    test_node = mock_v1_node()
    client.post(test_node)
    return test_node


def test_get_nodes():
    nodes = client.get("node")
    assert all(isinstance(node, NodeV1) for node in nodes)


def test_get_nodes_by_name():
    test_node = get_test_node()
    result = client.get("node", test_node.spec.name)
    assert len(result) == 1, result
    assert result[0].spec.name == test_node.spec.name


def test_get_nodes_by_name_namespace():
    test_node = get_test_node()
    result = client.get("node", test_node.spec.name, test_node.spec.namespace)
    assert result.spec.name == test_node.spec.name
    assert result.spec.namespace == test_node.spec.namespace


def test_get_nodes_by_namespace():
    test_node = get_test_node()
    result = client.get("node", "*", test_node.spec.namespace)
    assert isinstance(result, list)
    assert len(result) == 1  # node namespace is a uuid and therefore unique
    assert result[0].spec.name == test_node.spec.name
    assert result[0].spec.namespace == test_node.spec.namespace


def test_get_edges():
    result = client.get("edge")
    assert all(isinstance(edge, EdgeV1) for edge in result)


def test_post_node():
    test_node = mock_v1_node()
    result = client.post(test_node)
    assert isinstance(result, NodeV1)


def test_post_node_with_payload_options():
    test_node = mock_v1_node()
    options = {"payload": {"is_active": False}}
    result = client.post(test_node, options=options)
    assert result.spec.is_active is False


def test_post_edge():
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    client.post(test_nodes)
    result = client.post(test_edge)
    assert isinstance(result, EdgeV1)


def test_delete_node():
    test_node = mock_v1_node()
    test_node = client.post(test_node)
    assert client.get(test_node)
    client.delete(test_node)
    with pytest.raises(RequestException):
        result = client.get(test_node)


def test_delete_edge():
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    test_nodes = client.post(test_nodes)
    test_edge = client.post(test_edge)
    result = client.get(test_edge)
    assert result, result
    client.delete(test_edge)

    with pytest.raises(RequestException):
        result = client.get(test_edge)

    client.delete(test_nodes)


def test_patch_node():
    test_node = mock_v1_node()
    test_node = client.post(test_node)

    updated_node = test_node.update({"spec": {"is_active": True}})
    server_updated_node = client.patch(updated_node)
    assert server_updated_node == updated_node

    client.delete(test_node)


def test_patch_edge():
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    test_nodes = client.post(test_nodes)
    test_edge = client.post(test_edge)
    test_edge.spec.is_active = False
    server_updated_edge = client.patch(test_edge)
    assert server_updated_edge == test_edge

    client.delete(test_edge)
    client.delete(test_nodes)


def test_node_hash(client):
    test_node = mock_v1_node()
    test_node.spec.id = None
    new_node = client.post(test_node)
    assert hash(new_node) == hash(test_node)


def test_edge_hash(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    for obj in [test_edge, *test_nodes]:
        obj.spec.id = None
    client.post(test_nodes)
    new_edge = client.post(test_edge)
    assert hash(new_edge) == hash(test_edge)
