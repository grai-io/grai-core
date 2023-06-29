import pytest
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec

from grai_source_redshift.adapters import adapt_to_client
from grai_source_redshift.loader import RedshiftConnector
from grai_source_redshift.models import Column, Edge, Table


@pytest.fixture
def default_workspace():
    return WorkspaceSpec(name="default", organization="default")


@pytest.fixture
def mock_source(default_workspace):
    return SourceSpec(name="RedshiftTest", workspace=default_workspace)


@pytest.fixture
def connection() -> RedshiftConnector:
    """

    Args:

    Returns:

    Raises:

    """
    connection = RedshiftConnector(namespace="default")
    return connection


@pytest.fixture
def nodes_and_edges(tables, redshift_edges, mock_source):
    nodes = adapt_to_client(tables, mock_source, "v1")
    edges = adapt_to_client(redshift_edges, mock_source, "v1")
    return nodes, edges


@pytest.fixture
def nodes(nodes_and_edges):
    """

    Args:
        nodes_and_edges:

    Returns:

    Raises:

    """
    return nodes_and_edges[0]


@pytest.fixture
def edges(nodes_and_edges):
    """

    Args:
        nodes_and_edges:

    Returns:

    Raises:

    """
    return nodes_and_edges[1]


@pytest.fixture
def column_params():
    """ """
    column_params = [
        {
            "name": "test",
            "namespace": "test",
            "data_type": "integer",
            "is_nullable": True,
        },
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
    shared = {"table": "test_table", "schema": "test_schema"}
    for param in column_params:
        param.update(shared)
    return column_params


@pytest.fixture
def columns(column_params):
    """

    Args:
        column_params:

    Returns:

    Raises:

    """
    return [Column(**params) for params in column_params]


@pytest.fixture
def table_params(column_params):
    """

    Args:
        column_params:

    Returns:

    Raises:

    """
    table_params = [
        {"name": "test", "namespace": "test", "schema": "test"},
        {"table_name": "test", "namespace": "test", "table_schema": "test"},
        {"table_name": "test", "namespace": "test", "schema": "test"},
        {
            "name": "test",
            "schema": "test",
            "namespace": "test",
            "table_type": "BASE TABLE",
        },
        {"name": "test", "namespace": "test", "schema": "test", "columns": []},
        {"name": "test", "namespace": "test", "schema": "test", "metadata": {}},
        {
            "name": "test",
            "namespace": "test",
            "schema": "test",
            "table_type": "VIEW",
            "metadata": {},
            "columns": [],
        },
        {
            "table_name": "test2",
            "namespace": "test2",
            "table_schema": "test2",
            "name": "test2",
        },
    ]
    for param in table_params:
        param["table_dataset"] = "test"
        param.setdefault("table_type", "BASE TABLE")
    new_table = table_params[-1]
    new_table["columns"] = column_params
    table_params.append(new_table)
    return table_params


@pytest.fixture
def tables(table_params):
    """

    Args:
        table_params:

    Returns:

    Raises:

    """
    return [Table(**params) for params in table_params]


@pytest.fixture
def edge_params():
    """ """

    edge_params = [
        {
            "definition": "test",
            "constraint_type": "PRIMARY KEY",
            "destination": {
                "table_name": "test2",
                "namespace": "test2",
                "table_schema": "test2",
                "name": "test2",
            },
            "source": {
                "table_name": "test2",
                "namespace": "test2",
                "table_schema": "test2",
                "name": "test2",
            },
        },
        {
            "definition": "test",
            "constraint_type": "FOREIGN KEY",
            "destination": {
                "table_name": "test2",
                "namespace": "test2",
                "table_schema": "test2",
                "name": "test2",
            },
            "source": {
                "table_name": "test2",
                "namespace": "test2",
                "table_schema": "test2",
                "name": "test2",
            },
        },
    ]
    return edge_params


@pytest.fixture
def redshift_edges(edge_params):
    """

    Args:
        edge_params:

    Returns:

    Raises:

    """
    return [Edge(**params) for params in edge_params]
