import pytest
from dotenv import load_dotenv

from grai_source_fivetran.adapters import adapt_to_client
from grai_source_fivetran.loader import FivetranAPI, FivetranConnector
from grai_source_fivetran.mock_tools import MockFivetranObjects


# You may need to create a .env file to run these tests
@pytest.fixture
def api():
    return FivetranAPI()


@pytest.fixture
def app_nodes_and_edges():
    types_to_mock = ["cc", "ct", "tc", "tt"]
    edges = [MockFivetranObjects.mock_edge(t) for t in types_to_mock]
    nodes = []
    for edge in edges:
        nodes.append(edge.source)
        nodes.append(edge.destination)
    return nodes, edges


@pytest.fixture
def app_nodes(app_nodes_and_edges):
    return app_nodes_and_edges[0]


@pytest.fixture
def app_edges(app_nodes_and_edges):
    return app_nodes_and_edges[1]


@pytest.fixture
def nodes_and_edges(app_nodes_and_edges):
    nodes = adapt_to_client(app_nodes_and_edges[0], "v1")
    edges = adapt_to_client(app_nodes_and_edges[1], "v1")
    return nodes, edges


@pytest.fixture
def nodes(nodes_and_edges):
    return nodes_and_edges[0]


@pytest.fixture
def edges(nodes_and_edges):
    return nodes_and_edges[1]
