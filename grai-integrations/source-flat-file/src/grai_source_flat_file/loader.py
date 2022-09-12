import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union, Sequence
import pandas as pd
from grai_source_flat_file.models import ID, Column


def get_file_name(file_name: str) -> str:
    return os.path.splitext(file_name)[0]


def load_file(file_name: str) -> pd.DataFrame:
    assert file_name.endswith('.csv')
    return pd.read_csv(file_name)


def map_pandas_types(dtype):
    dtype = str(dtype).lower()
    if dtype.startswith('int'):
        return 'integer'
    elif dtype.startswith('float'):
        return 'float'
    elif dtype.startswith('object'):
        return 'string'


def build_column(data: pd.Series, namespace: str, table_name: str) -> Column:
    metadata = {
        'name': data.name,
        'namespace': namespace,
        'table': table_name,
        'data_type': map_pandas_types(data.dtype),
        'is_nullable': data.hasnans,
    }
    return Column(**metadata)


def column_builder(namespace: str, table_name: str):
    def inner(data: pd.Series) -> Column:
        return build_column(data, namespace, table_name)
    return inner


def get_nodes_and_edges(file_name: str, namespace: str):
    table_name = get_file_name(file_name)
    df = load_file(file_name)
    builder = column_builder(namespace, table_name)
    nodes = [builder(df[col]) for col in df.columns]
    return nodes, []

