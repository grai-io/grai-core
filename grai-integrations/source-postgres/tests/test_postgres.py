import os

import pytest

from grai_source_postgres.loader import PostgresConnector

# Tests only run with a separate postgres container deployed
# TODO: Mock the DB connection: https://blog.devgenius.io/creating-a-mock-database-for-unittesting-in-python-is-easier-than-you-think-c458e747224b
test_credentials = {
    "host": "localhost",
    "dbname": "grai",
    "user": "grai",
    "password": "grai",
    "port": "5432",
    "namespace": "test",
}


connection = PostgresConnector(**test_credentials)


def test_building_nodes():
    with connection.connect() as conn:
        tables = conn.tables

    assert len(tables) > 0


def test_building_edges():
    with connection.connect() as conn:
        edges = conn.foreign_keys

    assert len(edges) > 0, edges


def test_connector_from_env_vars():
    env_vars = {
        "GRAI_POSTGRES_HOST": "localhost",
        "GRAI_POSTGRES_DBNAME": "grai",
        "GRAI_POSTGRES_USER": "user",
        "GRAI_POSTGRES_PASSWORD": "pw",
        "GRAI_POSTGRES_NAMESPACE": "test",
        "GRAI_POSTGRES_PORT": "8000",
    }
    for k, v in env_vars.items():
        os.environ[k] = v

    conn = PostgresConnector()
    assert conn.host == "localhost"
    assert conn.port == "8000"
    assert conn.dbname == "grai"
    assert conn.user == "user"
    assert conn.password == "pw"
    assert conn.namespace == "test"
