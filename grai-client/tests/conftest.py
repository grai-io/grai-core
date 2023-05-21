import os

import pytest

from grai_client.endpoints.v1.client import ClientV1
from grai_client.testing.schema import (
    mock_v1_edge,
    mock_v1_edge_and_nodes,
    mock_v1_node,
)


@pytest.fixture(scope="session")
def client():
    host = os.environ.get("GRAI_HOST", "localhost")
    port = os.environ.get("GRAI_PORT", "8000")
    username = os.environ.get("GRAI_USERNAME", "null@grai.io")
    password = os.environ.get("GRAI_PASSWORD", "super_secret")
    workspace = os.environ.get("GRAI_WORKSPACE", "default")

    client = ClientV1(host, port, workspace=workspace, insecure=True)
    client.authenticate(username=username, password=password)
    return client


@pytest.fixture(scope="session")
def node_v1(client):
    test_node = mock_v1_node()
    test_node = client.post(test_node)
    return test_node


@pytest.fixture(scope="session")
def edge_v1(client):
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    nodes = client.post(test_nodes)
    edge = client.post(test_edge)
    return edge
