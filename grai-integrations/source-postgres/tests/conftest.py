import pytest

from grai_source_postgres.base import get_nodes_and_edges
from grai_source_postgres.loader import PostgresConnector


@pytest.fixture
def conn_credentials() -> dict:
    test_credentials = {
        "host": "localhost",
        "dbname": "grai",
        "user": "grai",
        "password": "grai",
        "port": "5433",
        "namespace": "test",
    }
    return test_credentials


@pytest.fixture
def connection(conn_credentials) -> PostgresConnector:
    """

    Args:

    Returns:

    Raises:

    """

    connection = PostgresConnector(**conn_credentials)
    return connection


@pytest.fixture
def nodes_and_edges(connection):
    """

    Args:
        connection:

    Returns:

    Raises:

    """
    nodes, edges = get_nodes_and_edges(connection, "v1")
    return nodes, edges
