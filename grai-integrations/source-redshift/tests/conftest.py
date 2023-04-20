import pytest

from grai_source_redshift.base import get_nodes_and_edges
from grai_source_redshift.loader import RedshiftConnector


@pytest.fixture
def connection() -> RedshiftConnector:
    test_credentials = {
        "host": "localhost",
        "dbname": "grai",
        "user": "grai",
        "password": "grai",
        "port": "5432",
        "namespace": "test",
    }

    connection = RedshiftConnector(**test_credentials)
    return connection


@pytest.fixture
def nodes_and_edges(connection):
    nodes, edges = get_nodes_and_edges(connection, "v1")
    return nodes, edges
