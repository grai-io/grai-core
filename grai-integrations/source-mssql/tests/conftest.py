import pytest

from grai_source_mssql.base import get_nodes_and_edges
from grai_source_mssql.loader import MySQLConnector


@pytest.fixture
def connection() -> MySQLConnector:
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
    nodes, edges = get_nodes_and_edges(connection, "v1")
    return nodes, edges
