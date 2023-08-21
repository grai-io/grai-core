import uuid

import pytest
from dotenv import dotenv_values
from grai_client.endpoints.v1.client import ClientV1
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec

from grai_source_cube.adapters import adapt_to_client
from grai_source_cube.base import MetabaseIntegration
from grai_source_cube.loader import MetabaseAPI, MetabaseConnector

config = dotenv_values(".env")


@pytest.fixture(scope="session")
def default_workspace():
    return WorkspaceSpec(name="default", organization="default")


@pytest.fixture(scope="session")
def mock_source(default_workspace):
    return SourceSpec(name=f"test-{uuid.uuid4()}", workspace=default_workspace)


@pytest.fixture(scope="session")
def client():
    try:
        client = ClientV1(url="http://localhost:8000", username="null@grai.io", password="super_secret")
    except:

        class MockClient:
            pass

        client = MockClient()
    return client


@pytest.fixture(scope="session")
def has_client(client):
    return isinstance(client, ClientV1)


@pytest.fixture(scope="session")
def connector_kwargs(mock_source):
    return {
        "username": config.get("grai_metabase_username", "admin@metabase.local"),
        "password": config.get("grai_metabase_password", "Metapass123"),
        "endpoint": config.get("grai_metabase_endpoint", "http://0.0.0.0:3001"),
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
def integration(connector_kwargs, mock_source):
    integration = MetabaseIntegration(source=mock_source, **connector_kwargs)
    return integration


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
