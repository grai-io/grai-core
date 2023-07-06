from typing import Any, Dict, List, Literal, Union, Sequence

from grai_schemas import config as base_config
from grai_schemas.schema import Schema
from grai_schemas.v1 import NodeV1, EdgeV1
from grai_schemas.v1.metadata.edges import (
    GenericEdgeMetadataV1,
    EdgeMetadataTypeLabels,
)
from grai_schemas.v1.metadata.nodes import (
    TableMetadata,
    NodeMetadataTypeLabels,
    GenericNodeMetadataV1,
)
from multimethod import multimethod

from grai_source_metabase.models import Table, Question, Edge, NodeTypes
from grai_source_metabase.package_definitions import config


def extract_grai_metadata(current, version):
    """
    Extracts the grai metadata from the build_metadata function for a given object.

    Args:
        current: The object to extract grai metadata from.
        version: The version of the metadata.

    Returns:
        Dict: The grai metadata extracted from the build_metadata function.

    Raises:
        None

    """

    metadata = build_metadata(current, version)
    if "schema" and "grai" in metadata.get("grai", None):
        metadata = metadata["grai"]

    return metadata


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    """
    Build grai metadata for a given object.

    Args:
        current (Any): The object to build grai metadata from.
        desired (Any): The desired format of the metadata.

    Returns:
        None: grai metadata object.

    Raises:
        NotImplementedError: If no adapter is available between the `current` and `desired` types.

    """

    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@build_grai_metadata.register
def build_grai_metadata_from_table(
    current: Table, version: Literal["v1"] = "v1"
) -> TableMetadata:
    """
    Build grai metadata for a Table object.

    Args:
        current (Table): The Table object to build grai metadata from.
        version (Literal["v1"], optional): The version of grai metadata to build. Defaults to "v1".

    Returns:
        TableMetadata: grai metadata object for the Table.

    Raises:
        None.

    """

    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.table.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return TableMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_question(
    current: Question, version: Literal["v1"] = "v1"
) -> GenericNodeMetadataV1:
    """
    Build grai metadata for a Question object.

    Args:
        current (Question): The Question object to build grai metadata from.
        version (Literal["v1"], optional): The version of grai metadata to build. Defaults to "v1".

    Returns:
        GenericNodeMetadataV1: grai metadata object for the Question.

    Raises:
        None.

    """

    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.generic.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return GenericNodeMetadataV1(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(
    current: Edge, version: Literal["v1"] = "v1"
) -> GenericEdgeMetadataV1:
    """
    Build grai metadata for an Edge object.

    Args:
        current (Edge): The Edge object to build grai metadata from.
        version (Literal["v1"], optional): The version of grai metadata to build. Defaults to "v1".

    Returns:
        GenericEdgeMetadataV1: grai metadata object for the Edge.

    Raises:
        None.

    """

    data = {
        "version": version,
        "edge_type": EdgeMetadataTypeLabels.generic.value,
        "tags": [config.metadata_id],
    }

    return GenericEdgeMetadataV1(**data)


@multimethod
def build_app_metadata(current: Any, desired: Any) -> None:
    """
    Build application-specific metadata for a given object.

    Args:
        current (Any): The object to build application-specific metadata from.
        desired (Any): The desired format of the metadata.

    Returns:
        None: Application-specific metadata object.

    Raises:
        NotImplementedError: If no adapter is available between the `current` and `desired` types.

    """

    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@build_app_metadata.register
def build_metadata_from_table(current: Table, version: Literal["v1"] = "v1") -> Dict:
    """
    Build application-specific metadata for a Table object.

    Args:
        current (Table): The Table object to build application-specific metadata from.
        version (Literal["v1"], optional): The version of the metadata to build. Defaults to "v1".

    Returns:
        Dict: Application-specific metadata object for the Table.

    Raises:
        None.

    """

    data = {
        "schema": current.schema_name,
    }

    return data


@build_app_metadata.register
def build_metadata_from_question(
    current: Question, version: Literal["v1"] = "v1"
) -> Dict:
    """
    Build application-specific metadata for a Question object.

    Args:
        current (Question): The Question object to build application-specific metadata from.
        version (Literal["v1"], optional): The version of the metadata to build. Defaults to "v1".

    Returns:
        Dict: Application-specific metadata object for the Question.

    Raises:
        None.

    """

    return {"name": current.name}


@build_app_metadata.register
def build_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> Dict:
    """
    Build application-specific metadata for an Edge object.

    Args:
        current (Edge): The Edge object to build application-specific metadata from.
        version (Literal["v1"], optional): The version of the metadata to build. Defaults to "v1".

    Returns:
        Dict: Application-specific metadata object for the Edge.

    Raises:
        None.

    """

    data = {
        "definition": current.definition,
    }

    data |= current.metadata if current.metadata is not None else {}

    return data


def build_metadata(obj, version):
    """
    Build metadata for a given object.

    Args:
        obj: The object to build metadata from.
        version: The version of the metadata to build.

    Returns:
        Dict: Metadata object containing both grai and application-specific metadata.

    Raises:
        None.

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
    Adapt a given object to the desired client format.

    Args:
        current (Any): The object to adapt.
        desired (Any): The desired format to adapt to.

    Returns:
        None: Adapted object in the desired format.

    Raises:
        NotImplementedError: If no adapter is available between the `current` and `desired` types.

    """

    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)}")


@adapt_to_client.register
def adapt_table_to_client(current: Table, version: Literal["v1"] = "v1") -> NodeV1:
    """
    Adapt a Table object to the desired client format.

    Args:
        current (Table): The Table object to adapt.
        version (Literal["v1"], optional): The version of the client format to adapt to. Defaults to "v1".

    Returns:
        NodeV1: Adapted Table object in the desired client format.

    Raises:
        None.

    """

    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": extract_grai_metadata(current, version),
    }

    # print("spec_dict_table", spec_dict)
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_question_to_client(
    current: Question, version: Literal["v1"] = "v1"
) -> NodeV1:
    """
    Adapt a Question object to the desired client format.

    Args:
        current (Question): The Question object to adapt.
        version (Literal["v1"], optional): The version of the client format to adapt to. Defaults to "v1".

    Returns:
        NodeV1: Adapted Question object in the desired client format.

    Raises:
        None.

    """

    # TODO: check if build_metadata has one grai key with correct values before passing it to metadata in spec_dict

    spec_dict = {
        "name": current.name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": extract_grai_metadata(current, version),
    }

    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: NodeTypes, node2: NodeTypes) -> str:
    """
    Creates a name for an edge based on the given nodes.

    Args:
        node1 (NodeTypes)
        node2 (NodeTypes)

    Returns:
        str: The name of the edge.

    Raises:
        None.
    """

    node1_fname = node1.full_name if isinstance(node1, Table) else node1.name
    node2_fname = node2.full_name if isinstance(node2, Table) else node2.name

    node1_name = f"{node1.namespace}:{node1_fname}"
    node2_name = f"{node2.namespace}:{node2_fname}"

    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: Literal["v1"] = "v1") -> EdgeV1:
    """
    Adapt an Edge object to the desired client format.

    Args:
        current (Edge): The Edge object to adapt.
        version (Literal["v1"], optional): The version of the client format to adapt to. Defaults to "v1".

    Returns:
        EdgeV1: Adapted Edge object in the desired client format.

    Raises:
        None.

    """

    spec_dict = {
        "data_source": config.integration_name,
        "name": make_name(current.source, current.destination),
        "namespace": current.source.namespace,
        "source": {
            "name": current.source.full_name
            if isinstance(current.source, Table)
            else current.source.name,
            "namespace": current.source.namespace,
        },
        "destination": {
            "name": current.destination.full_name
            if isinstance(current.destination, Table)
            else current.destination.name,
            "namespace": current.destination.namespace,
        },
        "metadata": extract_grai_metadata(current, version),
    }

    return Schema.to_model(spec_dict, version=version, typing_type="Edge")


@adapt_to_client.register
def adapt_seq_to_client(
    objs: Sequence, version: Literal["v1"]
) -> List[Union[NodeV1, EdgeV1]]:
    """
    Adapt a sequence of objects to the desired client format.

    Args:
        objs (Sequence): The sequence of objects to adapt.
        version (Literal["v1"]): The version of the client format to adapt to.

    Returns:
        List[Union[NodeV1, EdgeV1]]: Adapted sequence of objects in the desired client format.

    Raises:
        None.

    """

    return [adapt_to_client(item, version) for item in objs]


@adapt_to_client.register
def adapt_list_to_client(
    objs: List, version: Literal["v1"]
) -> List[Union[NodeV1, EdgeV1]]:
    """
    Adapt a list of objects to the desired client format.

    Args:
        objs (List): The list of objects to adapt.
        version (Literal["v1"]): The version of the client format to adapt to.

    Returns:
        List[Union[NodeV1, EdgeV1]]: Adapted list of objects in the desired client format.

    Raises:
        None.

    """

    return [adapt_to_client(item, version) for item in objs]
