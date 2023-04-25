import pytest

from grai_source_redshift.base import get_nodes_and_edges
from grai_source_redshift.loader import RedshiftConnector


@pytest.fixture
def connection() -> RedshiftConnector:
    connection = RedshiftConnector(namespace="default")
    return connection


@pytest.fixture
def nodes_and_edges(connection):
    nodes, edges = get_nodes_and_edges(connection, "v1")
    return nodes, edges


@pytest.fixture
def nodes(nodes_and_edges):
    return nodes_and_edges[0]


@pytest.fixture
def edges(nodes_and_edges):
    return nodes_and_edges[1]
