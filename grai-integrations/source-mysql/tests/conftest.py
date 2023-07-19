import pytest
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec

from grai_source_mysql.loader import MySQLConnector


@pytest.fixture
def default_workspace():
    return WorkspaceSpec(name="default", organization="default")


@pytest.fixture
def mock_source(default_workspace):
    return SourceSpec(name="BigQueryTest", workspace=default_workspace)


@pytest.fixture
def connection() -> MySQLConnector:
    """

    Args:

    Returns:

    Raises:

    """
    test_credentials = {
        "host": "localhost",
        "dbname": "grai",
        "user": "grai",
        "password": "grai",
        "namespace": "test",
    }

    connection = MySQLConnector(**test_credentials)
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
