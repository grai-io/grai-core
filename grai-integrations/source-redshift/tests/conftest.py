import pytest
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec

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


@pytest.fixture
def nodes_and_edges(connection):
    return [], []
    # """

    # Args:
    #     connection:

    # Returns:

    # Raises:

    # """
    # nodes, edges = get_nodes_and_edges(connection, "v1")
    # return nodes, edges


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
