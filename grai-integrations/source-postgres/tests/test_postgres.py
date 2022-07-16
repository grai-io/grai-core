import pytest
from grai_source_postgres.loader import PostgresConnector


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
    #assert False, tables




