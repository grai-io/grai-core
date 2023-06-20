from functools import cache
from uuid import UUID

import pytest
from grai_schemas.v1 import EdgeV1, NodeV1, WorkspaceV1
from grai_schemas.v1.edge import EdgeNamedID, EdgeUuidID
from grai_schemas.v1.mock import MockV1
from requests import RequestException

from grai_client.endpoints.utilities import is_valid_uuid
from grai_client.endpoints.v1.client import ClientV1
from grai_client.testing.schema import mock_v1_edge_and_nodes, mock_v1_node


def test_client_auth_from_init(client_params):
    client = ClientV1(**client_params)
    assert client.is_authenticated


def test_client_auth_from_authenticate(client_params):
    client_params = {**client_params}
    username, password = client_params.pop("username"), client_params.pop("password")
    client = ClientV1(**client_params)
    client.authenticate(username=username, password=password)
    assert client.is_authenticated


def test_client_has_workspace_uuid(client):
    assert isinstance(client.workspace, str) and is_valid_uuid(client.workspace)


def test_authentication(client):
    response = client.check_authentication()
    assert response.status_code == 200


def test_get_workspace_by_name(client):
    resp = client.get("workspace", name="default")
    assert len(resp) == 1
    assert isinstance(resp[0], WorkspaceV1)
    assert resp[0].spec.name == "default"


def test_get_workspace_by_ref(client):
    resp = client.get("workspace", ref="default/default")
    assert len(resp) == 1
    assert isinstance(resp[0], WorkspaceV1)
    assert resp[0].spec.ref == "default/default"


def test_get_workspaces(client):
    resp = client.get("workspace")
    for r in resp:
        assert isinstance(r, WorkspaceV1)


def test_post_workspace(client):
    workspace = WorkspaceV1(**MockV1.workspace_dict())
    resp = client.post(workspace)
    assert isinstance(resp, WorkspaceV1)
    assert resp == workspace


def test_get_nodes(client):
    nodes = client.get("node")
    assert all(isinstance(node, NodeV1) for node in nodes)


def test_get_nodes_by_name(client, node_v1):
    result = client.get("node", name=node_v1.spec.name)
    assert len(result) == 1, result
    assert result[0].spec.name == node_v1.spec.name


def test_get_nodes_by_name_namespace(client, node_v1):
    result = client.get("node", name=node_v1.spec.name, namespace=node_v1.spec.namespace)
    assert len(result) == 1, result
    assert result[0].spec.name == node_v1.spec.name
    assert result[0].spec.namespace == node_v1.spec.namespace


def test_get_nodes_by_namespace(client, node_v1):
    result = client.get("node", namespace=node_v1.spec.namespace)
    assert isinstance(result, list)
    assert len(result) == 1  # node namespace is a uuid and therefore unique
    assert result[0].spec.name == node_v1.spec.name
    assert result[0].spec.namespace == node_v1.spec.namespace


def test_get_edges(client):
    result = client.get("edge")
    assert all(isinstance(edge, EdgeV1) for edge in result)


def test_post_node(client):
    test_node = mock_v1_node()
    result = client.post(test_node)
    assert isinstance(result, NodeV1)


def test_post_node_with_payload_options(client):
    test_node = mock_v1_node()
    options = {"payload": {"is_active": False}}
    result = client.post(test_node, options=options)
    assert result.spec.is_active is False


def test_post_edge(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    client.post(test_nodes)
    result = client.post(test_edge)
    assert isinstance(result, EdgeV1)


def test_mixed_type_post(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    results = client.post([test_edge, *test_nodes])
    assert len(results) == 3
    assert all(isinstance(result, (EdgeV1, NodeV1)) for result in results)
    assert all(isinstance(result.spec.id, UUID) for result in results)


def test_delete_node(client):
    test_node = mock_v1_node()
    test_node = client.post(test_node)
    assert client.get(test_node)
    client.delete(test_node)
    with pytest.raises(RequestException):
        result = client.get(test_node)


def test_delete_edge(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    test_nodes = client.post(test_nodes)
    test_edge = client.post(test_edge)
    result = client.get(test_edge)
    assert result, result
    client.delete(test_edge)

    with pytest.raises(RequestException):
        result = client.get(test_edge)

    client.delete(test_nodes)


@pytest.mark.xfail(raises=RequestException, reason='Error: 404. Not Found. {"detail":"Not found."}')
def test_delete_mixed_type(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    objs = [test_edge, *test_nodes]
    objs = client.post(objs)
    client.delete(objs)
    _ = client.get(objs)


def test_patch_node(client):
    test_node = mock_v1_node()
    test_node = client.post(test_node)

    updated_node = test_node.update({"spec": {"is_active": True}})
    server_updated_node = client.patch(updated_node)
    assert server_updated_node == updated_node

    client.delete(test_node)


def test_patch_edge(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    test_nodes = client.post(test_nodes)
    test_edge = client.post(test_edge)
    test_edge.spec.is_active = False
    server_updated_edge = client.patch(test_edge)
    assert server_updated_edge == test_edge

    client.delete(test_edge)
    client.delete(test_nodes)


def test_patch_mixed_type(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    test_nodes = client.post(test_nodes)
    test_edge = client.post(test_edge)
    objs = [test_edge, *test_nodes]
    for obj in objs:
        obj.spec.is_active = False
    updated_objs = client.patch(objs)
    assert all(obj.spec.is_active is False for obj in updated_objs)


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


def test_get_edge_by_named_id(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    objs = client.post([*test_nodes, test_edge])

    identifier = EdgeNamedID(name=test_edge.spec.name, namespace=test_edge.spec.namespace)
    result = client.get(identifier)
    assert hash(result) == hash(test_edge), "Edge should be queryable by named id"


class TestSourceNode:
    @classmethod
    def setup_class(cls, client):
        cls.mocked_nodes = [MockV1.sourced_node_dict() for _ in range(10)]
        cls.mocked_nodes = client.post(cls.mocked_nodes)

    def test_get_by_label(self, client):
        source_node = MockV1.sourced_node_dict()
        source_node = client.post(source_node)
        result = client.get()
