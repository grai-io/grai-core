import os

import pytest
from grai_source_mysql.loader import MySQLConnector

# Tests only run with a separate mysql container deployed
# TODO: Mock the DB connection: 
test_credentials = {
    "host": "localhost",
    "dbname": "grai",
    "user": "grai",
    "password": "grai",
    "namespace": "test",
}


connection = MmSQLConnector(**test_credentials)


def test_building_nodes():
    with connection.connect() as conn:
        tables = conn.get_tables()

    assert len(tables) > 0


def test_building_edges():
    with connection.connect() as conn:
        edges = conn.get_foreign_keys()

    assert len(edges) > 0, edges


def test_connector_from_env_vars():
    env_vars = {
        "GRAI_MYSQL_HOST": "localhost",
        "GRAI_MYSQL_DBNAME": "grai",
        "GRAI_MYSQL_USER": "user",
        "GRAI_MYSQL_PASSWORD": "pw",
        "GRAI_MYSQL_NAMESPACE": "test",
        "GRAI_MYSQL_PORT": "8000",
    }
    for k, v in env_vars.items():
        os.environ[k] = v

    conn = MySQLConnector()
    assert conn.host == "localhost"
    assert conn.port == "8000"
    assert conn.dbname == "grai"
    assert conn.user == "user"
    assert conn.password == "pw"
    assert conn.namespace == "test"
