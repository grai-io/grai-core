import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import pandas as pd

from grai_source_flat_file.models import ID, Column, Edge, Table


def get_file_name(file_name: str) -> str:
    """

    Args:
        file_name (str):

    Returns:

    Raises:

    """
    return os.path.splitext(file_name)[0]


LOADER_MAP = {".csv": pd.read_csv, ".parquet": pd.read_parquet, ".feather": pd.read_feather}


def load_file(file_name: str) -> pd.DataFrame:
    """

    Args:
        file_name (str):

    Returns:

    Raises:

    """
    file_ext = os.path.splitext(file_name)[-1]
    assert file_ext in LOADER_MAP, f"{file_ext} not supported. Choose one of {set(LOADER_MAP.keys())}"
    return LOADER_MAP[file_ext](file_name)


def map_pandas_types(dtype) -> str:
    """

    Args:
        dtype:

    Returns:

    Raises:

    """
    dtype = str(dtype).lower()
    if dtype.startswith("int"):
        return "integer"
    elif dtype.startswith("float"):
        return "float"
    elif dtype.startswith("object"):
        return "string"
    else:
        return dtype


def build_column(data: pd.Series, namespace: str, table_name: str) -> Column:
    """

    Args:
        data (pd.Series):
        namespace (str):
        table_name (str):

    Returns:

    Raises:

    """
    metadata = {
        "name": data.name,
        "namespace": namespace,
        "table": table_name,
        "data_type": map_pandas_types(data.dtype),
        "is_nullable": data.hasnans,
    }
    return Column(**metadata)


def column_builder(namespace: str, table_name: str) -> Callable[[pd.Series], Column]:
    """

    Args:
        namespace (str):
        table_name (str):

    Returns:

    Raises:

    """

    def inner(data: pd.Series) -> Column:
        """

        Args:
            data (pd.Series):

        Returns:

        Raises:

        """
        return build_column(data, namespace, table_name)

    return inner


def table_builder(namespace: str, table_name: str, file_location: str) -> Table:
    """

    Args:
        namespace (str):
        table_name (str):
        file_location (str):

    Returns:

    Raises:

    """
    return Table(namespace=namespace, file_name=file_location, name=table_name)


def build_nodes_and_edges(file_name: str, namespace: str) -> Tuple[List[Union[Table, Column]], List[Edge]]:
    """

    Args:
        file_name (str):
        namespace (str):

    Returns:

    Raises:

    """
    table_name = get_file_name(file_name)
    df = load_file(file_name)

    builder = column_builder(namespace, table_name)
    columns = [builder(df[col]) for col in df.columns]

    table = table_builder(namespace, table_name, file_name)
    table.columns = columns

    nodes = [table, *columns]
    return nodes, table.get_edges()
