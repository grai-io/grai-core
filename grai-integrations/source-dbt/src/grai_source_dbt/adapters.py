from typing import Any, List, Literal, Sequence, Union

from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1
from grai_client.schemas.schema import Schema
from grai_source_dbt.models import Column, Edge, GraiNodeTypes, SupportedDBTTypes
from multimethod import multimethod


@multimethod
def adapt_to_client(current: Any, desired: Any) -> None:
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)}")


@adapt_to_client.register
def adapt_table_to_client(
    current: SupportedDBTTypes, version: Literal["v1"] = "v1"
) -> NodeV1:
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": "grai-dbt-adapter",
        "metadata": {
            "node_type": "Table",
            "description": current.description,
            "dbt_resource_type": current.resource_type,
            "dbt_materialization": current.config.materialized,
            "table_name": current.name,
            "dbt_model_name": current.unique_id,
        },
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_column_to_client(current: Column, version: Literal["v1"] = "v1") -> NodeV1:
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": "grai-postgres-adapter",
        "metadata": {
            "node_type": "Column",
            "description": current.description,
            "data_type": current.data_type,
            "dbt_tags": current.tags,
            "table_name": current.table_name,
            "dbt_quote": current.quote,
        },
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: GraiNodeTypes, node2: GraiNodeTypes) -> str:
    return f"{node1.full_name} -> {node2.full_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: Literal["v1"] = "v1") -> EdgeV1:
    metadata = {
        "definition": current.definition,
        "constraint_type": current.constraint_type.name,
    }

    spec_dict = {
        "data_source": "grai-dbt-adapter",
        "name": make_name(current.source, current.destination),
        "namespace": current.source.namespace,
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
    if current.metadata:
        metadata.update(current.metadata)
    return Schema.to_model(spec_dict, version=version, typing_type="Edge")


@adapt_to_client.register
def adapt_list_to_client(
    objs: Sequence, version: Literal["v1"]
) -> List[Union[NodeV1, EdgeV1]]:
    return [adapt_to_client(item, version) for item in objs]
