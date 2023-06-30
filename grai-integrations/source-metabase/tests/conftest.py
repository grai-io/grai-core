import pytest
from dotenv import dotenv_values

from src.grai_source_metabase.adapters import adapt_to_client
from src.grai_source_metabase.loader import MetabaseAPI
from src.grai_source_metabase.mock_tools import MockMetabaseObjects

config = dotenv_values(".env")


@pytest.fixture(scope="session")
def api():
    return MetabaseAPI()


@pytest.fixture
def connector_kwargs():
    return {
        "username": config["metabase_username"],
        "password": config["metabase_password"],
        "endpoint": "https://data.inv.tech/api/",
    }


@pytest.fixture
def app_nodes_and_edges():
    edges = [MockMetabaseObjects.mock_edge("tq")]
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
def nodes_and_edges(app_nodes_and_edges):
    """

    Args:
        app_nodes_and_edges:

    Returns:

    Raises:

    """
    nodes = adapt_to_client(app_nodes_and_edges[0], "v1")
    edges = adapt_to_client(app_nodes_and_edges[1], "v1")
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
