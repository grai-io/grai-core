from typing import Dict, List

import pytest

from grai_source_mssql.models import Column, Edge, Table

column_params = [
    {"name": "test", "namespace": "test", "data_type": "integer", "is_nullable": True},
    {
        "column_name": "test",
        "namespace": "test",
        "data_type": "integer",
        "is_nullable": True,
    },
    {
        "column_name": "test",
        "namespace": "test",
        "data_type": "integer",
        "is_nullable": True,
        "default_value": 2,
    },
    {
        "column_name": "test",
        "namespace": "test",
        "data_type": "integer",
        "is_nullable": True,
        "column_default": 2,
    },
]
shared = {"table": "test_table", "column_schema": "test_schema"}
for param in column_params:
    param.update(shared)


table_params: List[Dict] = [
    {"name": "test", "namespace": "test", "schema": "test"},
    {"table_name": "test", "namespace": "test", "table_schema": "test"},
    {"table_name": "test", "namespace": "test", "schema": "test"},
    {
        "name": "test",
        "schema": "test",
        "namespace": "test",
    },
    {"name": "test", "namespace": "test", "schema": "test", "columns": []},
    {"name": "test", "namespace": "test", "schema": "test", "metadata": {}},
    {
        "name": "test",
        "namespace": "test",
        "schema": "test",
        "metadata": {},
        "columns": [],
    },
]
new_table = table_params[-1]
new_table["columns"] = column_params
table_params.append(new_table)


def make_column_id():
    return {
        "table_schema": "schema",
        "table_name": "table",
        "name": "column",
        "namespace": "test",
    }


edge_params = [
    {
        "definition": "test",
        "constraint_type": "p",
        "destination": make_column_id(),
        "source": make_column_id(),
    },
    {
        "definition": "test",
        "constraint_type": "f",
        "destination": make_column_id(),
        "source": make_column_id(),
    },
]


@pytest.mark.parametrize("params", column_params)
def test_columns(params):
    table = Column(**params)
    assert isinstance(table, Column)


@pytest.mark.parametrize("params", table_params)
def test_tables(params):
    table = Table(**params)
    assert isinstance(table, Table)


@pytest.mark.parametrize("params", edge_params)
def test_edges(params):
    table = Edge(**params)
    assert isinstance(table, Edge)
