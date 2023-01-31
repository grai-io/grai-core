from typing import Any, Dict, List, Literal, Sequence, Union

from grai_schemas import config as grai_base_config
from grai_schemas.schema import Schema
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata.edges import (
    EdgeTypeLabels,
    GenericEdgeMetadataV1,
    TableToColumnMetadata,
)
from grai_schemas.v1.metadata.nodes import ColumnMetadata, NodeTypeLabels, TableMetadata
from multimethod import multimethod

from grai_source_dbt.models.nodes import (
    Column,
    Constraint,
    Edge,
    GraiNodeTypes,
    SupportedDBTTypes,
    Table,
)
from grai_source_dbt.package_definitions import config


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_grai_metadata.register
def build_grai_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> ColumnMetadata:
    data = {
        "version": version,
        "node_type": NodeTypeLabels.column.value,
        "node_attributes": {},
    }
    if current.data_type is not None:
        data["node_attributes"]["data_type"] = current.data_type

    return ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_node(current: SupportedDBTTypes, version: Literal["v1"] = "v1") -> TableMetadata:
    data = {"version": version, "node_type": NodeTypeLabels.table.value}

    return TableMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> GenericEdgeMetadataV1:
    data = {"version": version}

    if isinstance(current.source, Table) and isinstance(current.destination, Column):
        data["edge_type"] = EdgeTypeLabels.table_to_column.value
        return TableToColumnMetadata(**data)
    elif isinstance(current.source, Column) and isinstance(current.destination, Column):
        data["edge_type"] = EdgeTypeLabels.column_to_column.value
        return TableToTableMetadata(**data)
    else:
        data["edge_type"] = EdgeTypeLabels.generic.value
        return GenericEdgeMetadataV1(**data)


@multimethod
def build_dbt_metadata(current: Any, desired: Any) -> None:
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_dbt_metadata.register
def build_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> Dict:
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
def build_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> Dict:
    data = {
        "definition": current.definition,
        "constraint_type": current.constraint_type.name,
    }

    return data


@build_dbt_metadata.register
def build_metadata_from_node(current: SupportedDBTTypes, version: Literal["v1"] = "v1") -> Dict:
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
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@adapt_to_client.register
def adapt_table_to_client(current: SupportedDBTTypes, version: Literal["v1"] = "v1") -> NodeV1:
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

    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: GraiNodeTypes, node2: GraiNodeTypes) -> str:
    node1_name = f"{node1.namespace}:{node1.full_name}"
    node2_name = f"{node2.namespace}:{node2.full_name}"
    return f"{node1_name} -> {node2_name}"


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
        "metadata": {
            grai_base_config.metadata_id: build_grai_metadata(current, version),
            config.metadata_id: build_dbt_metadata(current, version),
        },
    }

    return Schema.to_model(spec_dict, version=version, typing_type="Edge")


@adapt_to_client.register
def adapt_list_to_client(objs: Sequence, version: Literal["v1"]) -> List[Union[NodeV1, EdgeV1]]:
    return [adapt_to_client(item, version) for item in objs]
