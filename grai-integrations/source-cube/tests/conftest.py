import os
import uuid

import dotenv
import pytest
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec
from grai_source_cube.api import CubeAPI
from grai_source_cube.base import CubeIntegration
from grai_source_cube.mock_tools import (
    MockConnector,
    MockCubeAPI,
    MockCubeIntegration,
    NamespaceMapFactory,
)
from grai_source_cube.settings import CubeApiConfig


@pytest.fixture(scope="session")
def default_workspace():
    return WorkspaceSpec(name="default", organization="default")


@pytest.fixture(scope="session")
def mock_source(default_workspace):
    return SourceSpec(name="CubeTest", workspace=default_workspace)


class MockClient:
    def __init__(self):
        self.id = "v1"

    def get(self, type, **kwargs):
        return [SourceSpec(id=uuid.uuid4(), **kwargs)]


@pytest.fixture(scope="session")
def client(mock_source):
    """ """
    try:
        from grai_client.endpoints.v1.client import ClientV1

        client = ClientV1(
            "localhost",
            "8000",
            insecure=True,
            username="null@grai.io",
            password="super_secret",
            workspace="default/default",
        )
        if not client.get("Source", name=mock_source.name):
            client.post(mock_source)
    except Exception:
        client = MockClient()

    return client


@pytest.fixture(scope="session")
def run_live(client) -> bool:
    has_client = not isinstance(client, MockClient)
    return has_client


# You may need to create a .env file to run these tests
@pytest.fixture(scope="session")
def env_config():
    """ """
    current_environ = set(os.environ)
    dotenv.load_dotenv()
    new_environ = set(os.environ)
    config = CubeApiConfig()

    for key in new_environ - current_environ:
        os.environ.pop(key)

    for key in current_environ:
        os.environ[key] = os.environ[key]

    return config


@pytest.fixture(scope="session")
def api(env_config):
    """ """
    return CubeAPI(config=env_config)


@pytest.fixture(scope="session")
def integration(request, env_config, mock_source):
    """ """
    request.config.cache.get("api-integration", None)  # can be used to cache api response results to avoid future calls
    namespace_map = {}
    return CubeIntegration(source=mock_source, config=env_config, namespace="test", namespace_map=namespace_map)


@pytest.fixture(scope="session")
def connector(integration):
    return integration.connector


@pytest.fixture
def config_args() -> dict:
    """ """

    return {
        "api_token": "test_key",
        "api_url": "https://www.cube.dev/v1",
        "api_secret": "test_secret",
    }


@pytest.fixture
def config(config_args):
    """ """
    return CubeApiConfig(**config_args)


@pytest.fixture(scope="session")
def namespace_map(run_live):
    return NamespaceMapFactory.build()


@pytest.fixture
def mock_api():
    return MockCubeAPI()


@pytest.fixture(scope="session")
def mock_connector():
    return MockConnector()


@pytest.fixture(scope="session")
def mock_integration():
    return MockCubeIntegration()


@pytest.fixture(scope="session")
def app_nodes_and_edges(connector):
    return connector.nodes, connector.edges


@pytest.fixture(scope="session")
def app_nodes(app_nodes_and_edges):
    return app_nodes_and_edges[0]


@pytest.fixture(scope="session")
def app_edges(app_nodes_and_edges):
    return app_nodes_and_edges[1]


@pytest.fixture(scope="session")
def nodes_and_edges(integration):
    return integration.get_nodes_and_edges()


@pytest.fixture(scope="session")
def nodes(nodes_and_edges):
    return nodes_and_edges[0]


@pytest.fixture(scope="session")
def edges(nodes_and_edges):
    """

    Args:
        nodes_and_edges:

    Returns:

    Raises:

    """
    return nodes_and_edges[1]
