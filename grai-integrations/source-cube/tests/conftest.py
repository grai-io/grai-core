import os
from typing import Optional

import dotenv
import pytest
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec
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


@pytest.fixture
def mock_api():
    return MockCubeAPI()


@pytest.fixture(scope="session")
def mock_connector():
    return MockConnector()


@pytest.fixture(scope="session")
def mock_integration():
    return MockCubeIntegration()


# You may need to create a .env file to run these tests
@pytest.fixture(scope="session")
def cloud_config() -> Optional[CubeApiConfig]:
    """ """
    current_environ = set(os.environ)
    dotenv.load_dotenv()
    new_environ = set(os.environ)
    try:
        config = CubeApiConfig()
    except Exception:
        config = None

    for key in new_environ - current_environ:
        os.environ.pop(key)

    for key in current_environ:
        os.environ[key] = os.environ[key]

    return config


@pytest.fixture(scope="session")
def cloud_integration(cloud_config, mock_source) -> Optional[CubeIntegration]:
    namespace_map = {}
    if cloud_config is None:
        return None

    return CubeIntegration(source=mock_source, config=cloud_config, namespace="test", namespace_map=namespace_map)


@pytest.fixture(scope="session")
def local_config() -> CubeApiConfig:
    return CubeApiConfig(api_url="http://localhost:4000/cubejs-api/v1", api_secret="secret")


@pytest.fixture(scope="session")
def local_integration(request, local_config, mock_source):
    """ """
    request.config.cache.get("api-integration", None)  # can be used to cache api response results to avoid future calls
    namespace_map = {}
    return CubeIntegration(source=mock_source, config=local_config, namespace="test", namespace_map=namespace_map)


@pytest.fixture(scope="session")
def config(local_integration):
    return local_integration.connector.config


@pytest.fixture(scope="session")
def namespace_map():
    return NamespaceMapFactory.build()


@pytest.fixture(scope="session")
def app_nodes_and_edges(local_integration):
    return local_integration.connector.nodes, local_integration.connector.edges


@pytest.fixture(scope="session")
def app_nodes(app_nodes_and_edges):
    return app_nodes_and_edges[0]


@pytest.fixture(scope="session")
def app_edges(app_nodes_and_edges):
    return app_nodes_and_edges[1]


@pytest.fixture(scope="session")
def nodes_and_edges(local_integration):
    return local_integration.get_nodes_and_edges()


@pytest.fixture(scope="session")
def nodes(nodes_and_edges):
    return nodes_and_edges[0]


@pytest.fixture(scope="session")
def edges(nodes_and_edges):
    return nodes_and_edges[1]
