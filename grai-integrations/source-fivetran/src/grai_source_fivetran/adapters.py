from typing import Any, Dict, List, Literal, Sequence, TypeVar, Union

from grai_schemas import config as base_config
from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1, SourceV1
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
from grai_schemas.v1.source import SourceSpec
from multimethod import multimethod

from grai_source_fivetran.models import Column, Edge, NodeTypes, Table
from grai_source_fivetran.package_definitions import config

T = TypeVar("T")
X = TypeVar("X")
Y = TypeVar("Y")


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
    # default_value = current.default_value
    # if current.default_value is not None:
    #     default_value = DefaultValue(
    #         has_default_value=True,
    #         default_value=current.default_value,
    #         data_type=current.data_type,
    #     )

    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.column.value,
        "node_attributes": {
            # "data_type": current.data_type,
            # "default_value": default_value,
            # "is_nullable": current.is_nullable,
            "is_primary_key": current.is_primary_key,
            # "is_unique": current.column_constraint and current.column_constraint.value in UNIQUE_COLUMN_CONSTRAINTS,
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

    if isinstance(current.source, Table):
        if isinstance(current.destination, Column):
            data["edge_type"] = EdgeMetadataTypeLabels.table_to_column.value
            return TableToColumnMetadata(**data)
        elif isinstance(current.destination, Table):
            data["edge_type"] = EdgeMetadataTypeLabels.table_to_table.value
            return TableToTableMetadata(**data)
    elif isinstance(current.source, Column):
        if isinstance(current.destination, Column):
            data["edge_type"] = EdgeMetadataTypeLabels.column_to_column.value
            data.update(
                {
                    "preserves_data_type": True,
                    "preserves_nullable": True,
                    "preserves_unique": True,
                }
            )
            return ColumnToColumnMetadata(**data)

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
def build_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Column):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "table_name": current.table_name,
        "schema": current.table_schema,
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
        "schema": current.schema_name,
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
    integration_meta["grai"] = build_grai_metadata(obj, version)

    return integration_meta


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
def adapt_column_to_client(current: Column, source: SourceSpec, version: Literal["v1"]) -> SourcedNodeV1:
    """

    Args:
        current:
        source:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": source,
        "metadata": build_metadata(current, version),
    }
    return SourcedNodeV1.from_spec(spec_dict)


@adapt_to_client.register
def adapt_table_to_client(current: Table, source: SourceSpec, version: Literal["v1"]) -> SourcedNodeV1:
    """

    Args:
        current:
        source:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": source,
        "metadata": build_metadata(current, version),
    }
    return SourcedNodeV1.from_spec(spec_dict)


def make_name(node1: NodeTypes, node2: NodeTypes) -> str:
    """

    Args:
        node1 (NodeTypes):
        node2 (NodeTypes):

    Returns:

    Raises:

    """
    node1_name = f"{node1.namespace}:{node1.full_name}"
    node2_name = f"{node2.namespace}:{node2.full_name}"
    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, source: SourceSpec, version: Literal["v1"]) -> SourcedEdgeV1:
    """

    Args:
        current:
        source:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "data_source": source,
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
    return SourcedEdgeV1.from_spec(spec_dict)


@adapt_to_client.register
def adapt_seq_to_client(
    objs: Sequence, source: SourceSpec, version: Literal["v1"]
) -> List[Union[SourcedNodeV1, SourcedEdgeV1]]:
    """

    Args:
        objs:
        version:

    Returns:

    Raises:

    """
    return [adapt_to_client(item, source, version) for item in objs]


@adapt_to_client.register
def adapt_list_to_client(
    objs: List, source: SourceSpec, version: Literal["v1"]
) -> List[Union[SourcedNodeV1, SourcedEdgeV1]]:
    """

    Args:
        objs:
        source:
        version:

    Returns:

    Raises:

    """
    return [adapt_to_client(item, source, version) for item in objs]


@adapt_to_client.register
def adapt_source_spec_v1_to_client(obj: X, source: SourceV1, version: Y) -> T:
    return adapt_to_client(obj, source.spec, version)
