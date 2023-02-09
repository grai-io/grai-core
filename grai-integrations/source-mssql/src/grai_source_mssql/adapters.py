from typing import Any, Dict, List, Literal, Sequence, Type

from grai_client.schemas.schema import Schema
from grai_schemas import config as base_config
from grai_schemas.generics import DefaultValue
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnMetadata,
    EdgeTypeLabels,
    GenericEdgeMetadataV1,
    TableToColumnMetadata,
    TableToTableMetadata,
)
from grai_schemas.v1.metadata.nodes import ColumnMetadata, NodeTypeLabels, TableMetadata
from multimethod import multimethod

from grai_source_mssql.models import (
    ID,
    UNIQUE_COLUMN_CONSTRAINTS,
    Column,
    ColumnConstraint,
    ColumnID,
    Edge,
    Table,
    TableID,
)
from grai_source_mssql.package_definitions import config


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_grai_metadata.register
def build_grai_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> ColumnMetadata:
    default_value = current.default_value
    if current.default_value is not None:
        default_value = DefaultValue(
            has_default_value=True,
            default_value=current.default_value,
            data_type=current.data_type,
        )

    data = {
        "version": version,
        "node_type": NodeTypeLabels.column.value,
        "node_attributes": {
            "data_type": current.data_type,
            "default_value": default_value,
            "is_nullable": current.is_nullable,
            "is_primary_key": current.column_constraint
            and current.column_constraint.value == ColumnConstraint.primary_key.value,
            "is_unique": current.column_constraint and current.column_constraint.value in UNIQUE_COLUMN_CONSTRAINTS,
        },
    }

    return ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_node(current: Table, version: Literal["v1"] = "v1") -> TableMetadata:
    data = {
        "version": version,
        "node_type": NodeTypeLabels.table.value,
        "node_attributes": {},
    }

    return TableMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> GenericEdgeMetadataV1:
    data = {"version": version}

    if isinstance(current.source, TableID):
        if isinstance(current.destination, ColumnID):
            data["edge_type"] = EdgeTypeLabels.table_to_column.value
            return TableToColumnMetadata(**data)
        elif isinstance(current.destination, TableID):
            data["edge_type"] = EdgeTypeLabels.table_to_table.value
            return TableToTableMetadata(**data)
    elif isinstance(current.source, ColumnID):
        if isinstance(current.destination, ColumnID):
            data["edge_type"] = EdgeTypeLabels.column_to_column.value
            return ColumnToColumnMetadata(**data)

    data["edge_type"] = EdgeTypeLabels.generic.value
    return GenericEdgeMetadataV1(**data)


@multimethod
def build_mysql_metadata(current: Any, desired: Any) -> None:
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_mysql_metadata.register
def build_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> Dict:
    data = {
        "table_name": current.table,
        "schema": current.column_schema,
    }

    return data


@build_mysql_metadata.register
def build_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> Dict:
    data = {
        "definition": current.definition,
        "constraint_type": current.constraint_type.name,
    }
    data |= current.metadata if current.metadata is not None else {}

    return data


@build_mysql_metadata.register
def build_metadata_from_node(current: Table, version: Literal["v1"] = "v1") -> Dict:
    data = {
        "schema": current.table_schema,
    }
    return data


def build_metadata(obj, version):
    return {
        base_config.metadata_id: build_grai_metadata(obj, version),
        config.metadata_id: build_mysql_metadata(obj, version),
    }


@multimethod
def adapt_to_client(current: Any, desired: Any):
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)}")


@adapt_to_client.register
def adapt_column_to_client(current: Column, version: Literal["v1"] = "v1"):
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_table_to_client(current: Table, version: Literal["v1"] = "v1"):
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: ID, node2: ID) -> str:
    node1_name = f"{node1.namespace}:{node1.full_name}"
    node2_name = f"{node2.namespace}:{node2.full_name}"
    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: Literal["v1"] = "v1"):
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
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Edge")


@adapt_to_client.register
def adapt_list_to_client(objs: Sequence, version: Literal["v1"]) -> List:
    return [adapt_to_client(item, version) for item in objs]
