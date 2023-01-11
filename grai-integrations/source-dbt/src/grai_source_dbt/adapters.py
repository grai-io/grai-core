from typing import Any, Dict, List, Literal, Sequence, Union

import grai_schemas.models as base_schemas
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1
from grai_client.schemas.schema import Schema
from grai_schemas import config as grai_base_config
from grai_schemas.models import DefaultValue, GraiNodeMetadata
from multimethod import multimethod

from grai_source_dbt.models.nodes import Column, Edge, GraiNodeTypes, SupportedDBTTypes
from grai_source_dbt.package_definitions import config


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@build_grai_metadata.register
def build_metadata_from_node(
    current: Column, version: Literal["v1"] = "v1"
) -> base_schemas.ColumnMetadata:
    data = {"version": version, "node_type": "Column", "node_attributes": {}}
    if current.data_type is not None:
        data["node_attributes"]["data_type"] = current.data_type

    return base_schemas.ColumnMetadata(**data)


@build_grai_metadata.register
def build_metadata_from_node(
    current: SupportedDBTTypes, version: Literal["v1"] = "v1"
) -> GraiNodeMetadata:
    data = {"version": version, "node_type": "Table", "node_attributes": {}}

    return base_schemas.TableMetadata(**data)


@multimethod
def build_dbt_metadata(current: Any, desired: Any) -> None:
    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@build_dbt_metadata.register
def build_metadata_from_node(current: Column, version: Literal["v1"] = "v1") -> Dict:
    data = {
        "description": current.description,
        "data_type": current.data_type,
        "dbt_tags": current.tags,
        "table_name": current.table_name,
        "dbt_quote": current.quote,
        "tests": [test.dict() for test in current.tests],
    }

    return data


@build_dbt_metadata.register
def build_metadata_from_node(current: Edge, version: Literal["v1"] = "v1") -> Dict:
    data = {
        "definition": current.definition,
        "constraint_type": current.constraint_type.name,
    }

    return data


@build_dbt_metadata.register
def build_metadata_from_node(
    current: SupportedDBTTypes, version: Literal["v1"] = "v1"
) -> Dict:
    data = {
        "description": current.description,
        "dbt_resource_type": current.resource_type,
        "dbt_materialization": current.config.materialized,
        "table_name": current.name,
        "dbt_model_name": current.unique_id,
    }
    if current.tests:
        data["tests"] = [test.dict() for test in current.tests]

    return data


@multimethod
def adapt_to_client(current: Any, desired: Any) -> None:
    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@adapt_to_client.register
def adapt_table_to_client(
    current: SupportedDBTTypes, version: Literal["v1"] = "v1"
) -> NodeV1:
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": {
            grai_base_config.metadata_id: build_grai_metadata(current, version),
            config.metadata_id: build_dbt_metadata(current, version),
        },
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_column_to_client(current: Column, version: Literal["v1"] = "v1") -> NodeV1:
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": {
            grai_base_config.metadata_id: build_grai_metadata(current, version),
            config.metadata_id: build_dbt_metadata(current, version),
        },
    }

    if current.tests:
        spec_dict["metadata"]["tests"] = [test.dict() for test in current.tests]

    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: GraiNodeTypes, node2: GraiNodeTypes) -> str:
    return f"{node1.full_name} -> {node2.full_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: Literal["v1"] = "v1") -> EdgeV1:
    spec_dict = {
        "data_source": config.integration_name,
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
        "metadata": {config.metadata_id: build_dbt_metadata(current, version)},
    }
    if current.metadata:
        metadata.update(current.metadata)
    return Schema.to_model(spec_dict, version=version, typing_type="Edge")


@adapt_to_client.register
def adapt_list_to_client(
    objs: Sequence, version: Literal["v1"]
) -> List[Union[NodeV1, EdgeV1]]:
    return [adapt_to_client(item, version) for item in objs]
