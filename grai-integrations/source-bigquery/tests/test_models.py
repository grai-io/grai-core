from typing import Dict, List

import pytest

from grai_source_bigquery.models import Column, Edge, Table


def test_columns(column_params):
    """

    Args:
        column_params:

    Returns:

    Raises:

    """
    for params in column_params:
        column = Column(**params)
        assert isinstance(column, Column)


def test_tables(table_params):
    """

    Args:
        table_params:

    Returns:

    Raises:

    """
    for params in table_params:
        table = Table(**params)
        assert isinstance(table, Table)


def test_edges(edge_params):
    """

    Args:
        edge_params:

    Returns:

    Raises:

    """
    for params in edge_params:
        table = Edge(**params)
        assert isinstance(table, Edge)
