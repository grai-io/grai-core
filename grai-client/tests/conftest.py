import os

import pytest
from grai_schemas.v1 import OrganisationV1, WorkspaceV1
from grai_schemas.v1.mock import MockV1

from grai_client.endpoints.v1.client import ClientV1


@pytest.fixture(scope="session")
def client_params():
    params = {
        "host": os.environ.get("GRAI_HOST", "localhost"),
        "port": os.environ.get("GRAI_PORT", "8000"),
        "username": os.environ.get("GRAI_USERNAME", "null@grai.io"),
        "password": os.environ.get("GRAI_PASSWORD", "super_secret"),
        "workspace": os.environ.get("GRAI_WORKSPACE", "default/default"),
        "insecure": True,
    }
    return params


@pytest.fixture(scope="session")
def client(client_params):
    host, port, username, password, workspace, insecure = (
        client_params["host"],
        client_params["port"],
        client_params["username"],
        client_params["password"],
        client_params["workspace"],
        client_params["insecure"],
    )

    client = ClientV1(host, port, workspace=workspace, insecure=insecure)
    client.authenticate(username=username, password=password)
    return client


@pytest.fixture(scope="session")
def workspace_v1(client):
    workspace = client.get("workspace", ref=f"default/default")[0]
    return workspace


@pytest.fixture(scope="session")
def mock_v1(workspace_v1):
    return MockV1(workspace=workspace_v1)


@pytest.fixture(scope="session")
def organisation_v1(client, workspace_v1):
    org = OrganisationV1.from_spec({"name": "default"})
    org.spec.id = workspace_v1.spec.organisation
    return org


@pytest.fixture(scope="session")
def source_v1(client, mock_v1, workspace_v1):
    test_source = MockV1().source.source_spec(workspace=workspace_v1.spec)
    source = client.post(test_source)
    return source


@pytest.fixture(scope="session")
def node_v1(client, mock_v1, source_v1):
    test_node = mock_v1.node.named_node_spec(data_sources=[source_v1.spec])
    return client.post(test_node)


@pytest.fixture(scope="session")
def edge_v1(client, mock_v1, source_v1):
    s_node = mock_v1.node.named_node_spec(data_sources=[source_v1.spec])
    d_node = mock_v1.node.named_node_spec(data_sources=[source_v1.spec])
    test_edge = mock_v1.edge.named_edge_spec(data_sources=[source_v1.spec], source=s_node, destination=d_node)
    _ = client.post([s_node, d_node])
    return client.post(test_edge)
