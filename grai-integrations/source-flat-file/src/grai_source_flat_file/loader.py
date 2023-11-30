import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import pandas as pd

from grai_source_flat_file.models import ID, Column, Edge, Table

LOADER_MAP = {".csv": pd.read_csv, ".parquet": pd.read_parquet, ".feather": pd.read_feather}


def load_file(file_name: str, file_ext: str) -> pd.DataFrame:
    """

    Args:
        file_name: The path to the file
        file_ext: The type of file

    Returns:

    Raises:

    """
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


def build_nodes_and_edges(
    file_ref: str, file_type: str, table_name: str, file_location: str, namespace: str
) -> Tuple[List[Union[Table, Column]], List[Edge]]:
    """

    Args:
        file_ref:
        file_type:
        table_name:
        file_location:
        namespace (str):

    Returns:

    Raises:

    """
    df = load_file(file_ref, file_type)

    builder = column_builder(namespace, table_name)
    columns = [builder(df[col]) for col in df.columns]

    table = table_builder(namespace, table_name, file_location)
    table.columns = columns

    nodes = [table, *columns]
    return nodes, table.get_edges()
