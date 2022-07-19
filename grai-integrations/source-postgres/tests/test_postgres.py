import pytest
from grai_source_postgres.loader import PostgresConnector

# Tests only run with a separate postgres container deployed
# TODO: Mock the DB connection: https://blog.devgenius.io/creating-a-mock-database-for-unittesting-in-python-is-easier-than-you-think-c458e747224b
test_credentials = {
    'host': 'localhost',
    'dbname': 'docker',
    'user': 'docker',
    'password': 'docker'
}


connection = PostgresConnector(**test_credentials)


def test_building_nodes():
    with connection.connect() as conn:
        tables = conn.get_tables()

    assert len(tables) > 0


def test_building_nodes():
    with connection.connect() as conn:
        nodes = conn.get_nodes()

    assert len(nodes) > 0


def test_building_edges():
    with connection.connect() as conn:
        edges = conn.get_foreign_keys()

    assert len(edges) > 0



