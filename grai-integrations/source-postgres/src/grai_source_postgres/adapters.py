from typing import Any, Dict, List, Sequence, Type

from grai_client.schemas.schema import Schema
from multimethod import multimethod

from grai_source_postgres.models import Column, Edge, Table


@multimethod
def adapt_to_client(current: Any, desired: Any):
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)}")


@adapt_to_client.register
def adapt_column_to_client(current: Column, version: str = "v1"):
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": "grai-postgres-adapter",
        "metadata": {
            "node_type": "Column",
            "is_pk": current.is_pk,
            "default_value": current.default_value,
            "is_nullable": current.is_nullable,
            "data_type": current.data_type,
            "table_name": current.table,
            "schema": current.schema,
        },
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_table_to_client(current: Table, version: str = "v1"):
    metadata = {
        "node_type": "Table",
        "schema": current.schema,
    }
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": "grai-postgres-adapter",
        "metadata": metadata,
    }
    metadata.update(current.metadata)
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: str = "v1"):
    metadata = {
        "definition": current.definition,
        "constraint_type": current.constraint_type,
    }

    spec_dict = {
        "data_source": "grai-postgres-adapter",
        "source": {
            "name": current.source.full_name,
            "namespace": current.source.namespace,
        },
        "destination": {
            "name": current.destination.full_name,
            "namespace": current.destination.namespace,
        },
        "metadata": metadata,
    }
    metadata.update(current.metadata)
    return Schema.to_model(spec_dict, version=version, typing_type="Edge")


@adapt_to_client.register
def adapt_list_to_client(objs: Sequence, version: str = "v1") -> List:
    return [adapt_to_client(item, version) for item in objs]


def update(client):
    client
