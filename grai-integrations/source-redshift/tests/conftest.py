import uuid

import pytest
from grai_schemas.v1.mock import MockV1
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec

from grai_source_redshift.base import RedshiftIntegration
from grai_source_redshift.loader import RedshiftConnector


@pytest.fixture
def default_workspace():
    return WorkspaceSpec(name="default", organization="default")


@pytest.fixture
def mock_source(default_workspace):
    return SourceSpec(name="RedshiftTest", workspace=default_workspace)


@pytest.fixture
def connection() -> RedshiftConnector:
    """

    Args:

    Returns:

    Raises:

    """
    connection = RedshiftConnector(namespace="default")
    return connection


class MockClient:
    def __init__(self):
        self.id = "v1"

    def get(self, type, **kwargs):
        return [SourceSpec(id=uuid.uuid4(), **kwargs)]


@pytest.fixture
def nodes_and_edges(mock_source):
    integration = RedshiftIntegration(source=mock_source, namespace="test")

    nodes, edges = integration.get_nodes_and_edges()
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
