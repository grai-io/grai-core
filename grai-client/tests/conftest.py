import pytest

from grai_client.testing.schema import (
    mock_v1_edge,
    mock_v1_edge_and_nodes,
    mock_v1_node,
)
from grai_client.utilities.tests import get_test_client


@pytest.fixture(scope="session")
def client():
    return get_test_client()


@pytest.fixture(scope="session")
def node_v1(client):
    test_node = mock_v1_node()
    client.post(test_node)
    return test_node
