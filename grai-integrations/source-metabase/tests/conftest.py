import pytest
from dotenv import dotenv_values
from grai_source_metabase.adapters import adapt_to_client
from grai_source_metabase.loader import MetabaseAPI, MetabaseConnector

config = dotenv_values(".env")


@pytest.fixture(scope="session")
def connector_kwargs():
    return {
        "username": config.get("grai_metabase_username", "admin@metabase.local"),
        "password": config.get("grai_metabase_password", "Metapass123"),
        "endpoint": config.get("grai_metabase_endpoint", "http://0.0.0.0:3000"),
        "metabase_namespace": config.get("grai_metabase_namespace", "metabase_grai"),
    }


@pytest.fixture(scope="session")
def api(connector_kwargs):
    return MetabaseAPI(**connector_kwargs)


@pytest.fixture(scope="session")
def connector(connector_kwargs):
    conn = MetabaseConnector(**connector_kwargs)
    return conn


@pytest.fixture(scope="session")
def app_nodes_and_edges(connector):
    nodes = connector.get_nodes()
    edges = connector.get_edges()
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
