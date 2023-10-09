from functools import partial
from typing import Any, Dict, List, Literal, Sequence, TypeVar, Union

from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1, SourceV1
from grai_schemas.v1.metadata.edges import (
    BaseEdgeMetadataV1,
    ColumnToColumnAttributes,
    ColumnToColumnMetadata,
    EdgeMetadataTypeLabels,
    GenericEdgeMetadataV1,
)
from grai_schemas.v1.metadata.nodes import (
    CollectionMetadata,
    ColumnMetadata,
    GenericNodeMetadataV1,
    NodeMetadataTypeLabels,
    QueryMetadata,
    TableMetadata,
)
from grai_schemas.v1.source import SourceSpec
from multimethod import multimethod
from pydantic import BaseModel

from grai_source_metabase.models import (
    Collection,
    Column,
    Edge,
    NodeTypes,
    Question,
    Table,
)
from grai_source_metabase.package_definitions import config

T = TypeVar("T")


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    """
    Build grai metadata for a given object.

    Args:
        current: The object to build grai metadata from.
        desired: The desired format of the metadata.

    Returns:
        None: grai metadata object.

    Raises:
        NotImplementedError: If no adapter is available between the `current` and `desired` types.

    """

    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_grai_metadata.register
def build_grai_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> ColumnMetadata:
    """
    Build grai metadata for a Table object.

    Args:
        current: The Table object to build grai metadata from.
        version: The version of grai metadata to build. Defaults to "v1".

    Returns:
        TableMetadata: grai metadata object for the Table.

    Raises:
        None.

    """

    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.column.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return ColumnMetadata(version=version, node_type=NodeMetadataTypeLabels.column.value, tags=[config.metadata_id])


@build_grai_metadata.register
def build_grai_metadata_from_table(current: Table, version: Literal["v1"] = "v1") -> TableMetadata:
    """
    Build grai metadata for a Table object.

    Args:
        current: The Table object to build grai metadata from.
        version: The version of grai metadata to build. Defaults to "v1".

    Returns:
        grai metadata object for the Table.

    Raises:
        None.

    """

    return TableMetadata(version=version, node_type=NodeMetadataTypeLabels.table.value, tags=[config.metadata_id])


@build_grai_metadata.register
def build_grai_metadata_from_question(current: Question, version: Literal["v1"] = "v1") -> QueryMetadata:
    """
    Build grai metadata for a Question object.

    Args:
        current (Question): The Question object to build grai metadata from.
        version (Literal["v1"], optional): The version of grai metadata to build. Defaults to "v1".

    Returns:
        grai metadata object for the Question.

    Raises:
        None.

    """

    return QueryMetadata(version=version, node_type=NodeMetadataTypeLabels.query.value, tags=[config.metadata_id])


@build_grai_metadata.register
def build_grai_metadata_from_collection(current: Collection, version: Literal["v1"] = "v1") -> CollectionMetadata:
    """
    Build grai metadata for a Collection object.

    Args:
        current: The Collection object to build grai metadata from.
        version: The version of grai metadata to build. Defaults to "v1".

    Returns:
        grai metadata object for the Collection.

    """

    return CollectionMetadata(
        version=version, node_type=NodeMetadataTypeLabels.collection.value, tags=[config.metadata_id]
    )


@build_grai_metadata.register
def build_grai_metadata_from_edge(
    current: Edge, version: Literal["v1"] = "v1"
) -> Union[ColumnToColumnMetadata, GenericEdgeMetadataV1]:
    """
    Build grai metadata for an Edge object.

    Args:
        current: The Edge object to build grai metadata from.
        version: The version of grai metadata to build. Defaults to "v1".

    Returns:
        Grai metadata object for the Edge.

    Raises:
        None.

    """
    tags = [config.metadata_id]

    if isinstance(current.source, Column):
        if isinstance(current.destination, Question):
            attributes = ColumnToColumnAttributes(
                version=version, preserves_data_type=True, preserves_nullable=True, preserves_unique=True
            )

            return ColumnToColumnMetadata(
                version=version,
                tags=tags,
                edge_type=EdgeMetadataTypeLabels.column_to_column.value,
                edge_attributes=attributes,
            )

    return GenericEdgeMetadataV1(version=version, tags=tags, edge_type=EdgeMetadataTypeLabels.generic.value)


@multimethod
def build_app_metadata(current: Any, desired: Any) -> None:
    """
    Build application-specific metadata for a given object.

    Args:
        current: The object to build application-specific metadata from.
        desired: The desired format of the metadata.

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
        current: The Table object to build application-specific metadata from.
        version: The version of the metadata to build. Defaults to "v1".

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
    integration_meta = build_app_metadata(obj, version)
    integration_meta["grai"] = build_grai_metadata(obj, version)

    return integration_meta


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
def adapt_table_to_client(
    current: Union[Table, Column], source: SourceSpec, version: Literal["v1"] = "v1"
) -> SourcedNodeV1:
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


@adapt_to_client.register
def adapt_collection_to_client(current: Collection, source: SourceSpec, version: Literal["v1"] = "v1") -> SourcedNodeV1:
    """
    Adapt a Collection object to the desired client format.
    Args:
        current:
        source:
        version:

    Returns:

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
    return [adapt_to_client(item, source, version) for item in objs]


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

    return [adapt_to_client(item, source, version) for item in objs]


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
