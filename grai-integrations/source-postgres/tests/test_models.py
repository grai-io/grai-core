from grai_source_postgres.models import Table, Column
import pytest


column_params = [
    {'name': 'test', 'data_type': 'integer', 'is_nullable': True},
    {'column_name': 'test', 'data_type': 'integer', 'is_nullable': True},
    {'column_name': 'test', 'data_type': 'integer', 'is_nullable': True,
     'default_value': 2},
    {'column_name': 'test', 'data_type': 'integer', 'is_nullable': True,
     'column_default': 2},
]


table_params = [
    {'name': 'test', 'table_schema': 'test'},
    {'table_name': 'test', 'table_schema': 'test'},
    {'table_name': 'test', 'schema': 'test'},
    {'name': 'test', 'schema': 'test'},
    {'name': 'test', 'schema': 'test', 'columns': []},
    {'name': 'test', 'schema': 'test', 'metadata': {}},
    {'name': 'test', 'schema': 'test', 'metadata': {}, 'columns': []},
]
new_table = table_params[-1]
new_table['columns'] = column_params
table_params.append(new_table)


@pytest.mark.parametrize('params', column_params)
def test_columns(params):
    table = Column(**params)
    assert isinstance(table, Column)


@pytest.mark.parametrize('params', table_params)
def test_tables(params):
    table = Table(**params)
    assert isinstance(table, Table)