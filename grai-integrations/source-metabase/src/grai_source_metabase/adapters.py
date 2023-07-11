from typing import Any, Dict, List, Literal, Sequence, TypeVar, Union

from grai_schemas import config as base_config
from grai_schemas.schema import Schema
from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1, SourceV1
from grai_schemas.v1.metadata.edges import EdgeMetadataTypeLabels, GenericEdgeMetadataV1
from grai_schemas.v1.metadata.nodes import (
    GenericNodeMetadataV1,
    NodeMetadataTypeLabels,
    QueryMetadata,
    TableMetadata,
)
from grai_schemas.v1.source import SourceSpec
from multimethod import multimethod
from pydantic import BaseModel

from grai_source_metabase.models import Edge, NodeTypes, Question, Table
from grai_source_metabase.package_definitions import config

T = TypeVar("T")


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

    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_grai_metadata.register
def build_grai_metadata_from_table(current: Table, version: Literal["v1"] = "v1") -> TableMetadata:
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
def build_grai_metadata_from_question(current: Question, version: Literal["v1"] = "v1") -> GenericNodeMetadataV1:
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
        "node_type": NodeMetadataTypeLabels.query.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return QueryMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> GenericEdgeMetadataV1:
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

    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_app_metadata.register
def build_metadata_from_table(current: BaseModel, version: Literal["v1"] = "v1") -> Dict:
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

    return {"raw_object": current.dict()}


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
        "metadata": current.metadata if current.metadata is not None else {},
        "raw_object": current.dict(),
    }

    return data


def build_metadata(obj, version) -> Dict[str, Dict]:
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
    return {
        base_config.metadata_id: build_grai_metadata(obj, version),
        config.metadata_id: build_app_metadata(obj, version),
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
def adapt_table_to_client(current: Table, source: SourceSpec, version: Literal["v1"] = "v1") -> SourcedNodeV1:
    """
    Adapt a Table object to the desired client format.

    Args:
        current: The Table object to adapt.
        source: The Source associated with the Table
        version: The version of the client format to adapt to. Defaults to "v1".

    Returns:
        NodeV1: Adapted Table object in the desired client format.

    Raises:
        None.

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
def adapt_question_to_client(current: Question, source: SourceSpec, version: Literal["v1"] = "v1") -> SourcedNodeV1:
    """
    Adapt a Question object to the desired client format.

    Args:
        current: The Question object to adapt.
        source: The source associated with the Question
        version: The version of the client format to adapt to. Defaults to "v1".

    Returns:
        NodeV1: Adapted Question object in the desired client format.

    Raises:
        None.

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
    Creates a name for an edge based on the given nodes.

    Args:
        node1 (NodeTypes)
        node2 (NodeTypes)

    Returns:
        str: The name of the edge.

    Raises:
        None.
    """

    node1_name = f"{node1.namespace}:{node1.full_name}"
    node2_name = f"{node2.namespace}:{node2.full_name}"

    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, source: SourceSpec, version: Literal["v1"] = "v1") -> SourcedEdgeV1:
    """
    Adapt an Edge object to the desired client format.

    Args:
        current: The Edge object to adapt.
        source: The data source associated with the Edge
        version: The version of the client format to adapt to. Defaults to "v1".

    Returns:
        EdgeV1: Adapted Edge object in the desired client format.

    Raises:
        None.

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
def adapt_seq_to_client(objs: Sequence, source: SourceSpec, version: Literal["v1"]) -> List[T]:
    """
    Adapt a sequence of objects to the desired client format.

    Args:
        objs: The sequence of objects to adapt.
        source: The source associated with each object in objs
        version: The version of the client format to adapt to.

    Returns:
        List[Union[NodeV1, EdgeV1]]: Adapted sequence of objects in the desired client format.

    Raises:
        None.

    """
    entities = [adapt_to_client(item, source, version) for item in objs]
    return list(entities)


@adapt_to_client.register
def adapt_list_to_client(objs: List, source: SourceSpec, version: Literal["v1"]) -> List[T]:
    """
    Adapt a list of objects to the desired client format.

    Args:
        objs: The list of objects to adapt.
        source: The source associated with each object in objs
        version: The version of the client format to adapt to.

    Returns:
        List[Union[NodeV1, EdgeV1]]: Adapted list of objects in the desired client format.

    Raises:
        None.

    """

    entities = [adapt_to_client(item, source, version) for item in objs]
    return list(entities)


@adapt_to_client.register
def adapt_source_v1_to_client(objs: Any, source: SourceV1, version: Any) -> List[T]:
    """
    Adapt a list of objects to the desired client format.

    Args:
        objs: The list of objects to adapt.
        source: The source associated with each object in objs
        version: The version of the client format to adapt to.

    Returns:
        List[Union[NodeV1, EdgeV1]]: Adapted list of objects in the desired client format.

    Raises:
        None.

    """

    return adapt_to_client(objs, source.spec, version)
