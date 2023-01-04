import os

import pytest
from grai_source_snowflake.loader import SnowflakeConnector

# Tests only run with a separate snowflake container deployed
# TODO: Mock the DB connection: https://blog.devgenius.io/creating-a-mock-database-for-unittesting-in-python-is-easier-than-you-think-c458e747224b
test_credentials = {
    "host": "localhost",
    "dbname": "docker",
    "user": "docker",
    "password": "docker",
    "port": "5433",
    "namespace": "test",
    "account": "test",
    "warehouse": "test",
}


connection = SnowflakeConnector(**test_credentials)


def test_building_nodes():
    with connection.connect() as conn:
        tables = conn.get_tables()

    assert len(tables) > 0, f"test expected more than {len(tables)} results"


def test_building_edges():
    with connection.connect() as conn:
        edges = conn.get_foreign_keys()

    assert len(edges) > 0, f"test expected more than {len(edges)} results"


def test_connector_from_env_vars():
    env_vars = {
        "GRAI_SNOWFLAKE_HOST": "localhost",
        "GRAI_SNOWFLAKE_DBNAME": "grai",
        "GRAI_SNOWFLAKE_USER": "user",
        "GRAI_SNOWFLAKE_PASSWORD": "pw",
        "GRAI_SNOWFLAKE_NAMESPACE": "test",
        "GRAI_SNOWFLAKE_PORT": "8000",
        "GRAI_SNOWFLAKE_ACCOUNT": "grai",
    }
    for k, v in env_vars.items():
        os.environ[k] = v

    conn = SnowflakeConnector()
    assert conn.host == "localhost"
    assert conn.port == "8000"
    assert conn.dbname == "grai"
    assert conn.user == "user"
    assert conn.password == "pw"
    assert conn.account == "grai"
    assert conn.namespace == "test"
