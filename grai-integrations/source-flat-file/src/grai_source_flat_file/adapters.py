from typing import Any, Dict, List, Literal, Sequence, Type, Union

from grai_schemas import config as base_config
from grai_schemas.generics import DefaultValue
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata.edges import EdgeTypeLabels, TableToColumnMetadata
from grai_schemas.v1.metadata.nodes import ColumnMetadata, NodeTypeLabels, TableMetadata
from multimethod import multimethod

from grai_source_flat_file.models import ID, Column, Edge, Table
from grai_source_flat_file.package_definitions import config


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
    data = {
        "version": version,
        "node_type": NodeTypeLabels.column.value,
        "node_attributes": {
            "data_type": current.data_type,
            "is_nullable": current.is_nullable,
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
        "node_type": NodeTypeLabels.table.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return TableMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> TableToColumnMetadata:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "version": version,
        "tags": [config.metadata_id],
    }
    return TableToColumnMetadata(edge_type=EdgeTypeLabels.table_to_column.value, **data)


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
        "table_name": current.table,
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
    data = {}
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
    data = {"file_name": current.file_name}
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
def adapt_column_to_client(current: Union[Table, Column], version: Literal["v1"] = "v1"):
    """

    Args:
        current (Union[Table, Column]):
        version (Literal["v1"], optional):  (Default value = "v1")

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
    return NodeV1.from_spec(spec_dict)


def make_name(node1: ID, node2: ID) -> str:
    """

    Args:
        node1 (ID):
        node2 (ID):

    Returns:

    Raises:

    """
    node1_name = f"{node1.namespace}.{node1.name}"
    node2_name = f"{node2.namespace}.{node2.name}"
    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_column_to_client(current: Edge, version: Literal["v1"] = "v1"):
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
    return EdgeV1.from_spec(spec_dict)


@adapt_to_client.register
def adapt_list_to_client(objs: Sequence, version: Literal["v1"] = "v1") -> List:
    """

    Args:
        objs (Sequence):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    return [adapt_to_client(item, version) for item in objs]
