from typing import Any, Dict, List, Literal, Sequence, Union
from warnings import warn

from grai_client.schemas.schema import Schema
from grai_schemas import config as base_config
from grai_schemas.generics import DefaultValue
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnMetadata,
    EdgeMetadataTypeLabels,
    GenericEdgeMetadataV1,
    TableToColumnMetadata,
    TableToTableMetadata,
)
from grai_schemas.v1.metadata.nodes import (
    ColumnMetadata,
    NodeMetadataTypeLabels,
    TableMetadata,
)
from multimethod import multimethod

from grai_source_redshift.models import (
    ID,
    UNIQUE_COLUMN_CONSTRAINTS,
    Column,
    ColumnConstraint,
    ColumnID,
    Constraint,
    Edge,
    LateBindingViewColumn,
    Table,
    TableID,
)
from grai_source_redshift.package_definitions import config


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_grai_metadata.register
def build_grai_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> ColumnMetadata:
    """

    Args:
        current (Column):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    default_value = current.default_value
    if current.default_value is not None:
        default_value = DefaultValue(
            has_default_value=True,
            default_value=current.default_value,
            data_type=current.data_type,
        )

    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.column.value,
        "node_attributes": {
            "data_type": current.data_type,
            "default_value": default_value,
            "is_nullable": None if current.is_nullable else False,  # Only not-nullable is definitive.
            "is_primary_key": current.column_constraint
            and current.column_constraint.value == ColumnConstraint.primary_key.value,
            "is_unique": current.column_constraint and current.column_constraint.value in UNIQUE_COLUMN_CONSTRAINTS,
        },
        "tags": [config.metadata_id],
    }

    return ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_column(current: LateBindingViewColumn, version: Literal["v1"] = "v1") -> ColumnMetadata:
    """

    Args:
        current (Column):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """

    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.column.value,
        "node_attributes": {
            "data_type": current.data_type,
        },
        "tags": [config.metadata_id],
    }

    return ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_node(current: Table, version: Literal["v1"] = "v1") -> TableMetadata:
    """

    Args:
        current (Table):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.table.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return TableMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> GenericEdgeMetadataV1:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {"version": version, "tags": [config.metadata_id]}

    if isinstance(current.source, TableID):
        if isinstance(current.destination, ColumnID):
            data["edge_type"] = EdgeMetadataTypeLabels.table_to_column.value
            return TableToColumnMetadata(**data)
        elif isinstance(current.destination, TableID):
            data["edge_type"] = EdgeMetadataTypeLabels.table_to_table.value
            return TableToTableMetadata(**data)
    elif isinstance(current.source, ColumnID):
        if isinstance(current.destination, ColumnID):
            data["edge_type"] = EdgeMetadataTypeLabels.column_to_column.value
            return ColumnToColumnMetadata(**data)

    message = (
        "No edge metadata implementation for edge with source type "
        f"{type(current.source)} and destination type {type(current.destination)}."
        "Fell back on generic metadata."
    )
    warn(message)
    data["edge_type"] = EdgeMetadataTypeLabels.generic.value
    return GenericEdgeMetadataV1(**data)


@multimethod
def build_app_metadata(current: Any, desired: Any) -> None:
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_app_metadata.register
def build_metadata_from_column(current: Union[Column, LateBindingViewColumn], version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Column):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "table_name": current.table,
        "schema": current.column_schema,
    }

    return data


@build_app_metadata.register
def build_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "definition": current.definition,
        "constraint_type": current.constraint_type.name,
    }
    data |= current.metadata if current.metadata is not None else {}

    return data


@build_app_metadata.register
def build_metadata_from_node(current: Table, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Table):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "schema": current.table_schema,
        "table_type": current.table_type.value,
    }

    return data


def build_metadata(obj, version):
    """

    Args:
        obj:
        version:

    Returns:

    Raises:

    """
    integration_meta = build_app_metadata(obj, version)
    base_metadata = build_grai_metadata(obj, version)
    integration_meta["grai"] = base_metadata

    return {
        base_config.metadata_id: base_metadata,
        config.metadata_id: integration_meta,
    }


@multimethod
def adapt_to_client(current: Any, desired: Any):
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)}")


@adapt_to_client.register
def adapt_column_to_client(current: Union[Table, Column, LateBindingViewColumn], version: Literal["v1"] = "v1"):
    """

    Args:
        current:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: ID, node2: ID) -> str:
    """

    Args:
        node1 (ID):
        node2 (ID):

    Returns:

    Raises:

    """
    node1_name = f"{node1.namespace}:{node1.full_name}"
    node2_name = f"{node2.namespace}:{node2.full_name}"
    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: Literal["v1"] = "v1"):
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
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
    """

    Args:
        objs (Sequence):
        version (Literal["v1"]):

    Returns:

    Raises:

    """
    return [adapt_to_client(item, version) for item in objs]
