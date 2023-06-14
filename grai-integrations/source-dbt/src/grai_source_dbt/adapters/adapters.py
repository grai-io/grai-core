from typing import Any, Dict, List, Literal, Sequence, Union

from grai_schemas import config as base_config
from grai_schemas import config as grai_base_config
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnMetadata,
    EdgeMetadataTypeLabels,
    GenericEdgeMetadataV1,
    TableToColumnMetadata,
    TableToTableMetadata,
)
from grai_schemas.v1.metadata.nodes import (
    ColumnAttributes,
    ColumnMetadata,
    NodeMetadataTypeLabels,
    TableMetadata,
)
from multimethod import multimethod

from grai_source_dbt.loaders import AllDbtNodeInstances, AllDbtNodeTypes
from grai_source_dbt.models.grai import Column, Constraint, Edge
from grai_source_dbt.package_definitions import config
from grai_source_dbt.utils import full_name


@multimethod
def build_grai_metadata(current: Any, version: Any) -> None:
    """

    Args:
        current (Any):
        version (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(
        f"No objects of type `{type(current)}` have no implementation of `build_grai_metadata` for version `{version}`."
    )


@build_grai_metadata.register
def build_grai_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> ColumnMetadata:
    """

    Args:
        current (Column):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    node_attributes: Dict[str, Union[bool, str]] = dict()
    if current.data_type is not None:
        node_attributes["data_type"] = current.data_type

    for test in current.tests:
        if test.test_metadata["name"] == "not_null":
            node_attributes["is_nullable"] = False
        elif test.test_metadata["name"] == "unique":
            node_attributes["is_unique"] = True
    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.column.value,
        "node_attributes": ColumnAttributes(**node_attributes),
        "tags": [config.metadata_id],
    }
    return ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_node(current: AllDbtNodeTypes, version: Literal["v1"] = "v1") -> TableMetadata:
    """

    Args:
        current (AllDbtNodeTypes):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {"version": version, "node_type": NodeMetadataTypeLabels.table.value, "tags": [config.metadata_id]}

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
    data = {"version": version, "edge_type": current.edge_type.value, "tags": [config.metadata_id]}
    if current.edge_type == EdgeMetadataTypeLabels.table_to_table:
        return TableToTableMetadata(**data)
    elif current.edge_type == EdgeMetadataTypeLabels.column_to_column:
        return ColumnToColumnMetadata(**data)
    elif current.edge_type == EdgeMetadataTypeLabels.table_to_column:
        return TableToColumnMetadata(**data)
    else:
        raise NotImplementedError(f"No supported metadata implementation for edge_type {current.edge_type.value}")


@multimethod
def build_app_metadata(current: Any, version: Any) -> None:
    """

    Args:
        current (Any):
        version (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(
        f"No objects of type `{type(current)}` have an implementation of `build_dbt_metadata` for version `{version}`."
    )


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
        "description": current.description,
        "data_type": current.data_type,
        "dbt_tags": current.tags,
        "table_name": current.table_name,
        "dbt_quote": current.quote,
        "tests": [test.dict() for test in current.tests],
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

    return data


@build_app_metadata.register
def build_metadata_from_node(current: AllDbtNodeTypes, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (AllDbtNodeTypes):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    return current.dict()


# ---


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
def adapt_to_client(current: Any, version: Any) -> None:
    """

    Args:
        current (Any):
        version (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No objects of type `{type(current)}` have a `{version}` client adapter.")


@adapt_to_client.register
def adapt_table_to_client(current: AllDbtNodeTypes, version: Literal["v1"] = "v1") -> NodeV1:
    """

    Args:
        current (AllDbtNodeTypes):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.grai_.full_name,
        "namespace": current.grai_.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version),
    }
    return NodeV1.from_spec(spec_dict)


@adapt_to_client.register
def adapt_column_to_client(current: Column, version: Literal["v1"] = "v1") -> NodeV1:
    """

    Args:
        current (Column):
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


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: Literal["v1"] = "v1") -> EdgeV1:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "data_source": config.integration_name,
        "name": current.name,
        "namespace": current.source.namespace,
        "source": {
            "name": current.source.name,
            "namespace": current.source.namespace,
        },
        "destination": {
            "name": current.destination.name,
            "namespace": current.destination.namespace,
        },
        "metadata": build_metadata(current, version),
    }

    return EdgeV1.from_spec(spec_dict)


@adapt_to_client.register
def adapt_list_to_client(objs: Sequence, version: Literal["v1"]) -> List[Union[NodeV1, EdgeV1]]:
    """

    Args:
        objs (Sequence):
        version (Literal["v1"]):

    Returns:

    Raises:

    """
    return [adapt_to_client(item, version) for item in objs]


@adapt_to_client.register
def adapt_to_client_default_version(obj: Any):
    """

    Args:
        obj (Any):

    Returns:

    Raises:

    """
    return adapt_to_client(obj, version="v1")
