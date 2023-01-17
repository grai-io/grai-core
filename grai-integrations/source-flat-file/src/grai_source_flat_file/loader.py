import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import pandas as pd

from grai_source_flat_file.models import ID, Column, Edge, Table


def get_file_name(file_name: str) -> str:
    return os.path.splitext(file_name)[0]


def load_file(file_name: str) -> pd.DataFrame:
    assert file_name.endswith(".csv"), file_name
    return pd.read_csv(file_name)


def map_pandas_types(dtype) -> str:
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
    metadata = {
        "name": data.name,
        "namespace": namespace,
        "table": table_name,
        "data_type": map_pandas_types(data.dtype),
        "is_nullable": data.hasnans,
    }
    return Column(**metadata)


def column_builder(namespace: str, table_name: str) -> Callable[[pd.Series], Column]:
    def inner(data: pd.Series) -> Column:
        return build_column(data, namespace, table_name)

    return inner


def table_builder(namespace: str, table_name: str, file_location: str) -> Table:
    return Table(namespace=namespace, file_name=file_location, name=table_name)


def build_nodes_and_edges(
    file_name: str, namespace: str
) -> Tuple[List[Union[Table, Column]], List[Edge]]:
    table_name = get_file_name(file_name)
    df = load_file(file_name)

    builder = column_builder(namespace, table_name)
    columns = [builder(df[col]) for col in df.columns]

    table = table_builder(namespace, table_name, file_name)
    table.columns = columns

    nodes = [table, *columns]
    return nodes, table.get_edges()
