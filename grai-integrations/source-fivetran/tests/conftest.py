import uuid

import dotenv
import pytest
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec

from grai_source_fivetran.adapters import adapt_to_client
from grai_source_fivetran.base import FivetranIntegration
from grai_source_fivetran.loader import FivetranAPI
from grai_source_fivetran.mock_tools import MockFivetranObjects

dotenv.load_dotenv()


@pytest.fixture(scope="session")
def default_workspace():
    return WorkspaceSpec(name="default", organization="default")


@pytest.fixture(scope="session")
def mock_source(default_workspace):
    return SourceSpec(name="BigQueryTest", workspace=default_workspace)


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
    except:
        client = MockClient()

    return client


@pytest.fixture(scope="session")
def run_live(client) -> bool:
    has_client = not isinstance(client, MockClient)
    has_local_api_creds = False
    try:
        FivetranAPI()
        has_local_api_creds = True
    except:
        import warnings

        warnings.warn("MISSING FIVETRAN CREDENTIALS. Not all tests will be able to run without these. .")

    return has_client and has_local_api_creds


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


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def namespace_map(run_live):
    if run_live:
        api = FivetranAPI()
        namespace_map = {
            conn.id: {"source": str(uuid.uuid4()), "destination": str(uuid.uuid4())} for conn in api.get_connectors()
        }
        return namespace_map
    else:
        return {}


@pytest.fixture(scope="session")
def nodes_and_edges(app_nodes_and_edges, client, mock_source, run_live, namespace_map):
    """

    Args:
        app_nodes_and_edges:
        client:
        mock_source:
        run_live:
        namespace_map:

    Returns:

    Raises:

    """
    if run_live:
        integration = FivetranIntegration(source=mock_source, namespaces=namespace_map)
        nodes, edges = integration.get_nodes_and_edges()
    else:
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
