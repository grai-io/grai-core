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
def organisation_v1(client):
    return OrganisationV1.from_spec({"name": "default"})


@pytest.fixture(scope="session")
def workspace_v1(client, organisation_v1):
    workspace = client.get("workspace", ref=f"{organisation_v1.spec.name}/default")[0]
    return workspace


@pytest.fixture(scope="session")
def source_v1(client, workspace_v1):
    test_source = MockV1.source.source(workspace=workspace_v1.spec.dict())
    source = client.post(test_source)
    return source


@pytest.fixture(scope="session")
def node_v1(client, source_v1):
    test_node = MockV1.node.node(data_sources=[source_v1.spec])
    test_node = client.post(test_node)
    return test_node


@pytest.fixture(scope="session")
def edge_v1(client, source_v1):
    test_edge, test_nodes = MockV1.edge.edge_and_nodes(data_sources=[source_v1.spec])
    nodes = client.post(test_nodes)
    edge = client.post(test_edge)
    return edge
