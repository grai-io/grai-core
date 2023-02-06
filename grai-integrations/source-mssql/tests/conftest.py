import pytest

from grai_source_mssql.base import get_nodes_and_edges
from grai_source_mssql.loader import MsSQLConnector


@pytest.fixture
def connection() -> MsSQLConnector:
    test_credentials = {
        "server": "localhost,1433",
        "user": "sa",
        "password": "GraiGraiGr4i",
        "namespace": "test",
        "encrypt": False,
    }

    connection = MsSQLConnector(**test_credentials)
    return connection


@pytest.fixture
def nodes_and_edges(connection):
    nodes, edges = get_nodes_and_edges(connection, "v1")
    return nodes, edges
