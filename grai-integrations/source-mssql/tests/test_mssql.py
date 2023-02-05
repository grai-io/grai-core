import os

import pytest
from grai_schemas.v1 import EdgeV1, NodeV1

from grai_source_mssql.adapters import adapt_to_client
from grai_source_mssql.loader import MsSQLConnector
from grai_source_mssql.models import Column, ColumnID, Edge, Table

tables = [
    Table(
        name="test",
        namespace="tests",
        table_schema="test",
        columns=[],
        metadata={"thing": "here"},
    )
]
table_values = [(item, "v1", NodeV1) for item in tables]


def test_building_tables(connection):
    with connection.connect() as conn:
        result = conn.tables

    assert len(result) > 0
    result_names = {r.name for r in result}
    assert "table1" in result_names, result_names
    assert "table2" in result_names, result_names


def test_building_columns(connection):
    with connection.connect() as conn:
        result = conn.columns

    assert len(result) > 0


def test_building_foreign_keys(connection):
    with connection.connect() as conn:
        result = conn.foreign_keys

    assert len(result) > 0


def test_building_nodes(connection):
    with connection.connect() as conn:
        result = conn.get_nodes()
    assert len(result) > 0


def test_building_edges(connection):
    with connection.connect() as conn:
        result = conn.get_edges()

    assert len(result) > 0


@pytest.mark.filterwarnings("ignore:Specified driver")
def test_connector_from_env_vars():
    env_vars = {
        "GRAI_MSSQL_DATABASE": "localhost",
        "GRAI_MSSQL_SERVER": "grai",
        "GRAI_MSSQL_USER": "sa",
        "GRAI_MSSQL_PASSWORD": "GraiGraiGr4i",
        "GRAI_MSSQL_NAMESPACE": "test",
        "GRAI_MSSQL_DRIVER": "{This is an invalid driver configuration}",
        "GRAI_MSSQL_TRUSTED_CONNECTION": "true",
    }
    for k, v in env_vars.items():
        os.environ[k] = v

    conn = MsSQLConnector()
    assert conn.config.driver == "{This is an invalid driver configuration}"
    assert conn.config.database == "localhost"
    assert conn.config.user == "sa"
    assert conn.config.password.get_secret_value() == "GraiGraiGr4i"
    assert conn.config.trusted_connection is True
    assert conn.config.namespace == "test"
