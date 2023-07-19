from functools import cache
from uuid import UUID, uuid4

import pytest
from grai_schemas.v1 import EdgeV1, NodeV1, SourcedNodeV1, SourceV1, WorkspaceV1
from grai_schemas.v1.edge import EdgeNamedID, EdgeUuidID, SourcedEdgeSpec, SourcedEdgeV1
from grai_schemas.v1.metadata.metadata import (
    GraiEdgeMetadataV1,
    GraiNodeMetadataV1,
    MetadataV1,
)
from grai_schemas.v1.mock import MockV1
from requests import RequestException

from grai_client.endpoints.utilities import is_valid_uuid
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.utils import MockClientV1
from grai_client.errors import NotSupportedError, ObjectNotFoundError


def build_mocked_node(client, mock_v1, **kwargs):
    data_sources = [mock_v1.source.source_spec() for i in range(2)]
    data_sources = [source.spec for source in client.post(data_sources)]
    node_spec = mock_v1.node.named_node_spec(data_sources=data_sources, **kwargs)
    node = mock_v1.node.node(spec=node_spec)

    return node


def build_mocked_edge(client, mock_v1, source=None, destination=None, **kwargs):
    if source is None:
        source = client.post(build_mocked_node(client, mock_v1))
    if destination is None:
        destination = client.post(build_mocked_node(client, mock_v1))

    data_sources = [mock_v1.source.source_spec() for i in range(2)]
    data_sources = [source.spec for source in client.post(data_sources)]
    edge_spec = mock_v1.edge.named_edge_spec(
        source=source.spec, destination=destination.spec, data_sources=data_sources, **kwargs
    )
    edge = mock_v1.edge.edge(spec=edge_spec)
    return edge, [source, destination]


class TestClientV1:
    @staticmethod
    def test_client_auth_from_init(client_params):
        client = ClientV1(**client_params)
        assert client.is_authenticated

    @staticmethod
    def test_client_auth_from_authenticate(client_params):
        client_params = {**client_params}
        username, password = client_params.pop("username"), client_params.pop("password")
        client = ClientV1(**client_params)
        client.authenticate(username=username, password=password)
        assert client.is_authenticated

    @staticmethod
    def test_client_has_workspace_uuid(client):
        assert isinstance(client.workspace, str) and is_valid_uuid(client.workspace)

    @staticmethod
    def test_authentication(client):
        response = client.check_authentication()
        assert response.status_code == 200

    @staticmethod
    def test_mock_client():
        client = MockClientV1()
        assert isinstance(client, ClientV1)


class TestWorkspaceV1:
    @staticmethod
    def test_get_all_workspaces(client):
        resp = client.get("workspace")
        assert isinstance(resp, list)
        for r in resp:
            assert isinstance(r, WorkspaceV1)

    @staticmethod
    def test_post_workspace(client, workspace_v1, organisation_v1, mock_v1):
        workspace = mock_v1.workspace.workspace_spec(organisation=organisation_v1.spec)
        workspace.ref = f"{organisation_v1.spec.name}/{workspace.name}"
        resp = client.post(workspace)
        assert isinstance(resp, WorkspaceV1)
        assert resp.spec.ref == workspace.ref
        assert resp.spec.name == workspace.name

    @staticmethod
    @pytest.mark.xfail(raises=NotSupportedError)
    def test_delete_workspace(client, workspace_v1, mock_v1):
        workspace = mock_v1.workspace.workspace(organisation=workspace_v1.spec)
        client.delete(workspace)

    @staticmethod
    @pytest.mark.xfail(raises=NotSupportedError)
    def test_patch_workspace(client, workspace_v1, mock_v1):
        workspace = mock_v1.workspace.workspace_spec(organisation=workspace_v1.spec)
        resp = client.patch(workspace)

    @staticmethod
    def test_get_workspace_by_workspace_v1(client, workspace_v1):
        resp = client.get(workspace_v1)
        assert isinstance(resp, WorkspaceV1)
        assert resp.spec.name == workspace_v1.spec.name
        assert resp.spec.ref == workspace_v1.spec.ref

    @staticmethod
    def test_get_workspace_by_workspace_spec(client, workspace_v1):
        resp = client.get(workspace_v1.spec)
        assert isinstance(resp, WorkspaceV1)
        assert resp.spec.name == workspace_v1.spec.name
        assert resp.spec.ref == workspace_v1.spec.ref

    @staticmethod
    def test_get_missing_workspace_by_workspace_v1(client, organisation_v1, mock_v1):
        workspace = mock_v1.workspace.workspace_spec(organisation=organisation_v1.spec)

        with pytest.raises(ObjectNotFoundError):
            resp = client.get(workspace)


class TestSourceV1:
    @staticmethod
    def test_get_all_sources(client):
        resp = client.get("source")
        assert isinstance(resp, list)
        for r in resp:
            assert isinstance(r, SourceV1)

    @staticmethod
    def test_post_source_v1(client, mock_v1):
        test_source = mock_v1.source.source_spec(workspace=client.workspace)
        resp = client.post(test_source)
        assert isinstance(resp, SourceV1)
        assert resp.spec.name == test_source.name

    @staticmethod
    def test_patch_source_v1(client, mock_v1):
        test_source = mock_v1.source.source_spec(workspace=client.workspace)
        test_source = client.post(test_source)
        test_source.spec.name = str(uuid4())
        resp = client.patch(test_source)
        assert isinstance(resp, SourceV1)
        assert resp.spec.name == test_source.spec.name
        assert resp.spec.workspace == test_source.spec.workspace

    @staticmethod
    def test_delete_source_v1(client, mock_v1):
        test_source = mock_v1.source.source_spec(workspace=client.workspace)
        test_source = client.post(test_source)
        client.delete(test_source)

        with pytest.raises(ObjectNotFoundError):
            client.get(test_source)

    @staticmethod
    def test_get_source_by_source_v1(client, mock_v1):
        test_source = mock_v1.source.source_spec(workspace=client.workspace)
        test_source = client.post(test_source)
        resp = client.get(test_source)
        assert isinstance(resp, SourceV1)
        assert resp.spec.name == test_source.spec.name
        assert resp.spec.workspace == test_source.spec.workspace

    @staticmethod
    def test_get_source_by_source_spec(client, mock_v1):
        test_source = mock_v1.source.source_spec(workspace=client.workspace)
        test_source = client.post(test_source)
        resp = client.get(test_source.spec)
        assert isinstance(resp, SourceV1)
        assert resp.spec.name == test_source.spec.name
        assert resp.spec.workspace == test_source.spec.workspace

    @staticmethod
    def test_get_missing_source(client, mock_v1):
        test_source = mock_v1.source.source_spec(workspace=client.workspace)

        with pytest.raises(ObjectNotFoundError):
            client.get(test_source)

    @staticmethod
    def test_patch_missing_source_v1(client, mock_v1):
        test_source = mock_v1.source.source(workspace=client.workspace)
        test_source.spec.id = uuid4()
        with pytest.raises(ObjectNotFoundError):
            resp = client.patch(test_source)


class TestOrganisationV1:
    @staticmethod
    @pytest.mark.xfail(raises=NotSupportedError)
    def test_get_all_organisations(client):
        resp = client.get("Organisation")

    @staticmethod
    @pytest.mark.xfail(raises=NotSupportedError)
    def test_get_organisation(client, mock_v1):
        org = mock_v1.organisation.organisation()
        resp = client.get(org)

    @staticmethod
    @pytest.mark.xfail(raises=NotSupportedError)
    def test_post_organisation(client, mock_v1):
        org = mock_v1.organisation.organisation()
        resp = client.post(org)

    @staticmethod
    @pytest.mark.xfail(raises=NotSupportedError)
    def test_get_organisation(client, mock_v1):
        org = mock_v1.organisation.organisation()
        resp = client.patch(org)

    @staticmethod
    @pytest.mark.xfail(raises=NotSupportedError)
    def test_delete_organisation(client, mock_v1):
        org = mock_v1.organisation.organisation()
        resp = client.delete(org)


class TestNodesV1:
    @staticmethod
    def test_get_nodes(client):
        nodes = client.get("node")
        assert all(isinstance(node, NodeV1) for node in nodes)
        assert all(isinstance(node.spec.metadata, MetadataV1) for node in nodes)

    @classmethod
    def test_post_node(cls, client, mock_v1):
        test_node = build_mocked_node(client, mock_v1)
        sources_names = {s.name for s in test_node.spec.data_sources}

        result = client.post(test_node)

        assert isinstance(result, NodeV1)
        assert result.spec.name == test_node.spec.name
        assert result.spec.namespace == test_node.spec.namespace
        assert result.spec.is_active == test_node.spec.is_active

        assert len(result.spec.data_sources) == len(sources_names)
        for data_source in result.spec.data_sources:
            assert data_source.name in sources_names

    @classmethod
    def test_patch_node(cls, client, mock_v1):
        test_node = build_mocked_node(client, mock_v1)
        test_node = client.post(test_node)

        updated_node = test_node.update({"spec": {"is_active": True}})
        server_updated_node = client.patch(updated_node)
        assert server_updated_node == updated_node

        client.delete(test_node)

    @classmethod
    def test_get_node_by_node_spec(cls, client, mock_v1):
        test_node = build_mocked_node(client, mock_v1)
        test_node = client.post(test_node)
        result = client.get(test_node.spec)
        assert isinstance(result, NodeV1)
        assert result.spec.name == test_node.spec.name
        assert result.spec.namespace == test_node.spec.namespace

    @classmethod
    def test_get_node_by_node_v1(cls, client, mock_v1):
        test_node = build_mocked_node(client, mock_v1)
        test_node = client.post(test_node)
        result = client.get(test_node)
        assert isinstance(result, NodeV1)
        assert result.spec.name == test_node.spec.name
        assert result.spec.namespace == test_node.spec.namespace

    @staticmethod
    def test_get_missing_node(client, mock_v1):
        test_node = mock_v1.node.node()
        with pytest.raises(ObjectNotFoundError):
            client.get(test_node)

    @classmethod
    def test_delete_node(cls, client, mock_v1):
        test_node = build_mocked_node(client, mock_v1)
        result = client.post(test_node)
        client.delete(test_node)
        with pytest.raises(ObjectNotFoundError):
            result = client.get(test_node)

    @classmethod
    def test_post_node_with_payload_options(cls, client, mock_v1):
        test_node = build_mocked_node(client, mock_v1)
        options = {"payload": {"is_active": False}}
        result = client.post(test_node, options=options)
        assert result.spec.is_active is False

    @classmethod
    def test_post_node_hash_unchanged(cls, client, mock_v1):
        test_node = build_mocked_node(client, mock_v1)
        test_node.spec.id = None
        new_node = client.post(test_node)
        assert hash(new_node) == hash(test_node)


class TestEdgesV1:
    @staticmethod
    def test_get_edges(client):
        result = client.get("edge")
        assert all(isinstance(edge, EdgeV1) for edge in result)
        assert all(isinstance(edge.spec.metadata, MetadataV1) for edge in result)

    @staticmethod
    def test_post_edge(client, mock_v1):
        test_edge, nodes = build_mocked_edge(client, mock_v1)
        result = client.post(test_edge)
        assert isinstance(result, EdgeV1)

    @staticmethod
    def test_mixed_type_post(client, mock_v1):
        test_edge, nodes = build_mocked_edge(client, mock_v1)
        client.delete(nodes)
        results = client.post([test_edge, *nodes])
        assert len(results) == 3
        assert all(isinstance(result, (EdgeV1, NodeV1)) for result in results)
        assert all(isinstance(result.spec.id, UUID) for result in results)

    @staticmethod
    def test_delete_edge(client, mock_v1):
        test_edge, nodes = build_mocked_edge(client, mock_v1)
        test_edge = client.post(test_edge)
        client.delete(test_edge)

        with pytest.raises(ObjectNotFoundError):
            result = client.get(test_edge)

    @staticmethod
    def test_delete_mixed_type(client, mock_v1):
        test_edge, nodes = build_mocked_edge(client, mock_v1)
        objs = client.post(test_edge)
        client.delete(objs)

        with pytest.raises(ObjectNotFoundError):
            result = client.get(objs)

    @staticmethod
    def test_patch_edge(client, mock_v1):
        test_edge, test_nodes = build_mocked_edge(client, mock_v1)
        test_edge = client.post(test_edge)

        test_edge.spec.is_active = False
        server_updated_edge = client.patch(test_edge)
        assert server_updated_edge == test_edge

        client.delete(test_edge)
        client.delete(test_nodes)

    @staticmethod
    def test_patch_mixed_type(client, mock_v1):
        test_edge, test_nodes = build_mocked_edge(client, mock_v1)
        test_edge = client.post(test_edge)
        objs = [test_edge, *test_nodes]
        for obj in objs:
            obj.spec.is_active = False
        updated_objs = client.patch(objs)
        assert all(obj.spec.is_active is False for obj in updated_objs)

    @staticmethod
    def test_edge_hash(client, mock_v1):
        test_edge, test_nodes = build_mocked_edge(client, mock_v1)

        test_edge.spec.id = None
        new_edge = client.post(test_edge)

        assert hash(new_edge) == hash(test_edge)

    @staticmethod
    def test_get_edge_by_named_id(client, mock_v1):
        test_edge, test_nodes = build_mocked_edge(client, mock_v1)
        objs = client.post(test_edge)

        identifier = EdgeNamedID(name=test_edge.spec.name, namespace=test_edge.spec.namespace)
        result = client.get(identifier)
        assert hash(result) == hash(test_edge), "Edge should be queryable by named id"


@pytest.fixture(scope="module")
def source_node_source(client, mock_v1):
    source = client.post(mock_v1.source.source())
    return source


@pytest.fixture(scope="module")
def source_node_init_nodes(client, mock_v1, source_node_source):
    init_specs = [mock_v1.node.named_source_node_spec(data_source=source_node_source.spec) for i in range(3)]
    init_nodes = client.post(init_specs)
    return init_nodes


class TestSourceNodeV1:
    def mocked_node(self, source, mock_v1):
        node_spec = mock_v1.node.named_source_node_spec(data_source=source.spec)
        return SourcedNodeV1.from_spec(node_spec)

    def test_get_by_label(self, client, source_node_source, source_node_init_nodes):
        source_nodes = client.get("SourceNode", source_node_source.spec.id)
        assert len(source_nodes) == len(source_node_init_nodes)
        for node in source_nodes:
            assert isinstance(node, SourcedNodeV1)
            assert isinstance(node.spec.metadata, GraiNodeMetadataV1)

    def test_get_by_node_source_v1(self, client, source_node_init_nodes):
        test_node = source_node_init_nodes[0]
        node = client.get(test_node)
        assert node.spec.name == test_node.spec.name
        assert node.spec.namespace == test_node.spec.namespace

    def test_get_by_node_spec(self, client, source_node_init_nodes):
        test_node = source_node_init_nodes[0]
        node = client.get(test_node.spec)
        assert node.spec.name == test_node.spec.name
        assert node.spec.namespace == test_node.spec.namespace

    def test_post_source_node(self, client, source_node_source, mock_v1):
        test_node = self.mocked_node(source_node_source, mock_v1)
        result = client.post(test_node)
        assert isinstance(result, SourcedNodeV1)
        assert isinstance(result.spec.metadata, GraiNodeMetadataV1)
        assert result.spec.id is not None
        assert result.spec.name == test_node.spec.name
        assert result.spec.namespace == test_node.spec.namespace

    def test_delete_source_node(self, client, source_node_source, mock_v1):
        test_node = self.mocked_node(source_node_source, mock_v1)
        result = client.post(test_node)
        client.delete(result)
        with pytest.raises(ObjectNotFoundError):
            result = client.get(result)

    def test_patch_source_node(self, client, source_node_source, mock_v1):
        test_node = self.mocked_node(source_node_source, mock_v1)
        result = client.post(test_node)
        result.spec.is_active = False
        result = client.patch(result)
        assert result.spec.is_active is False

    def test_patch_missing_source_node(self, client, source_node_source, mock_v1):
        test_node = self.mocked_node(source_node_source, mock_v1)
        result = client.post(test_node)
        client.delete(result)
        with pytest.raises(ObjectNotFoundError):
            result = client.patch(result)

    def test_patch_missing_source_node_by_name(self, client, source_node_source, mock_v1):
        test_node = self.mocked_node(source_node_source, mock_v1)
        result = client.post(test_node)
        client.delete(result)

        with pytest.raises(Exception):
            result = client.patch(test_node.spec)

    def test_source_node_hash(self, client, source_node_source, mock_v1):
        test_node = self.mocked_node(source_node_source, mock_v1)
        test_node.spec.id = None
        new_node = client.post(test_node)
        assert hash(new_node) == hash(test_node)


@pytest.fixture(scope="module")
def source_edge_source(client, mock_v1):
    source = client.post(mock_v1.source.source())
    return source


@pytest.fixture(scope="module")
def initial_source_edge_test_values(client, source_edge_source, mock_v1):
    mock_nodes = []
    mock_edges = []
    sources = [source_edge_source.spec]
    for _ in range(3):
        nodes = [mock_v1.node.named_node_spec(data_sources=sources) for i in range(2)]
        edge = mock_v1.edge.named_edge_spec(source=nodes[0], destination=nodes[1], data_sources=sources)
        mock_nodes.extend(nodes)
        mock_edges.append(edge)

    init_nodes = client.post(mock_nodes)
    init_edges = client.post(mock_edges)
    return init_nodes, init_edges


@pytest.fixture(scope="module")
def source_edge_init_edge(initial_source_edge_test_values):
    init_nodes, init_edges = initial_source_edge_test_values
    return init_edges


@pytest.fixture(scope="module")
def source_edge_init_node(initial_source_edge_test_values):
    init_nodes, init_edges = initial_source_edge_test_values
    return init_nodes


class TestSourceEdgeV1:
    def mocked_edge(self, source, mock_v1):
        s_node = mock_v1.node.named_source_node_spec(data_source=source.spec)
        d_node = mock_v1.node.named_source_node_spec(data_source=source.spec)
        spec = mock_v1.edge.named_source_edge_spec(data_source=source.spec, source=s_node, destination=d_node)
        return mock_v1.edge.sourced_edge(spec=spec)

    def test_get_by_label(self, client, source_edge_source, source_edge_init_edge):
        source_edges = client.get("SourceEdge", source_edge_source.spec.id)
        assert len(source_edges) == len(source_edge_init_edge)
        for node in source_edges:
            assert isinstance(node, SourcedEdgeV1)
            assert isinstance(node.spec.metadata, GraiEdgeMetadataV1)

    def test_get_by_source_edge_v1(self, client, source_edge_init_edge):
        test_edge = source_edge_init_edge[0]
        edge = client.get(test_edge)
        assert edge.spec.name == test_edge.spec.name
        assert edge.spec.namespace == test_edge.spec.namespace

    def test_get_by_source_edge_spec(self, client, source_edge_init_edge):
        test_edge = source_edge_init_edge[0]
        edge = client.get(test_edge.spec)
        assert edge.spec.name == test_edge.spec.name
        assert edge.spec.namespace == test_edge.spec.namespace

    def test_post_source_edge(self, client, source_edge_source, mock_v1):
        test_edge = self.mocked_edge(source_edge_source, mock_v1)
        client.post([test_edge.spec.source, test_edge.spec.destination])
        edge = client.post(test_edge)
        assert isinstance(edge, SourcedEdgeV1)
        assert isinstance(edge.spec.metadata, GraiEdgeMetadataV1)
        assert edge.spec.id is not None
        assert edge.spec.name == test_edge.spec.name
        assert edge.spec.namespace == test_edge.spec.namespace

    def test_delete_source_edge(self, client, source_edge_source, mock_v1):
        test_edge = self.mocked_edge(source_edge_source, mock_v1)
        client.post([test_edge.spec.source, test_edge.spec.destination])
        edge = client.post(test_edge)
        client.delete(edge)
        with pytest.raises(ObjectNotFoundError):
            client.get(edge)

    def test_patch_source_edge(self, client, source_edge_source, mock_v1):
        test_edge = self.mocked_edge(source_edge_source, mock_v1)
        client.post([test_edge.spec.source, test_edge.spec.destination])
        edge = client.post(test_edge)
        edge.spec.is_active = False
        edge = client.patch(edge)
        assert edge.spec.is_active is False

    def test_patch_missing_source_edge(self, client, source_edge_source, mock_v1):
        test_edge = self.mocked_edge(source_edge_source, mock_v1)
        client.post([test_edge.spec.source, test_edge.spec.destination])
        edge = client.post(test_edge)
        client.delete(edge)
        with pytest.raises(ObjectNotFoundError):
            client.patch(edge)

    def test_patch_missing_source_edge_by_name(self, client, source_edge_source, mock_v1):
        test_edge = self.mocked_edge(source_edge_source, mock_v1)
        client.post([test_edge.spec.source, test_edge.spec.destination])
        edge = client.post(test_edge)
        client.delete(edge)
        with pytest.raises(Exception):
            client.patch(test_edge.spec)

    def test_source_edge_hash(self, client, source_edge_source, mock_v1):
        test_edge = self.mocked_edge(source_edge_source, mock_v1)
        client.post([test_edge.spec.source, test_edge.spec.destination])
        test_edge.spec.id = None
        new_edge = client.post(test_edge)
        assert hash(new_edge) == hash(test_edge)
