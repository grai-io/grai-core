import os

import pytest

from grai_source_postgres.loader import PostgresConnector


def test_building_nodes(connection):
    """ """
    with connection.connect() as conn:
        tables = conn.tables

    assert len(tables) > 0


def test_building_edges(connection):
    """ """
    with connection.connect() as conn:
        edges = conn.foreign_keys

    assert len(edges) > 0, edges


def test_connector_from_env_vars():
    """ """
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
