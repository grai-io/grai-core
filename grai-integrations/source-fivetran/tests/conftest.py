import pytest
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec

from grai_source_fivetran.adapters import adapt_to_client
from grai_source_fivetran.loader import FivetranAPI, FivetranConnector
from grai_source_fivetran.mock_tools import MockFivetranObjects


@pytest.fixture
def default_workspace():
    return WorkspaceSpec(name="default", organization="default")


@pytest.fixture
def mock_source(default_workspace):
    return SourceSpec(name="BigQueryTest", workspace=default_workspace)


# You may need to create a .env file to run these tests
@pytest.fixture(scope="session")
def api():
    """ """
    return FivetranAPI()


@pytest.fixture
def connector_kwargs():
    """ """
    return {
        "api_key": "test_key",
        "api_secret": "test_secret",
        "endpoint": "http://www.fivetran.com/",
    }


@pytest.fixture
def app_nodes_and_edges():
    """ """
    types_to_mock = ["cc", "ct", "tc", "tt"]
    edges = [MockFivetranObjects.mock_edge(t) for t in types_to_mock]
    nodes = []
    for edge in edges:
        nodes.append(edge.source)
        nodes.append(edge.destination)
    return nodes, edges


@pytest.fixture
def app_nodes(app_nodes_and_edges):
    """

    Args:
        app_nodes_and_edges:

    Returns:

    Raises:

    """
    return app_nodes_and_edges[0]


@pytest.fixture
def app_edges(app_nodes_and_edges):
    """

    Args:
        app_nodes_and_edges:

    Returns:

    Raises:

    """
    return app_nodes_and_edges[1]


@pytest.fixture
def nodes_and_edges(app_nodes_and_edges, mock_source):
    """

    Args:
        app_nodes_and_edges:

    Returns:

    Raises:

    """
    nodes = adapt_to_client(app_nodes_and_edges[0], mock_source, "v1")
    edges = adapt_to_client(app_nodes_and_edges[1], mock_source, "v1")
    return nodes, edges


@pytest.fixture
def nodes(nodes_and_edges):
    """

    Args:
        nodes_and_edges:

    Returns:

    Raises:

    """
    return nodes_and_edges[0]


@pytest.fixture
def edges(nodes_and_edges):
    """

    Args:
        nodes_and_edges:

    Returns:

    Raises:

    """
    return nodes_and_edges[1]
