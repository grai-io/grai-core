import copy
from typing import Any, Dict, Optional, Union

from grai_schemas.generics import MalformedMetadata, Metadata
from grai_schemas.utilities import merge
from grai_schemas.v1.edge import EdgeSpec, EdgeV1, SourcedEdgeSpec, SourcedEdgeV1
from grai_schemas.v1.generics import Code
from grai_schemas.v1.metadata.edges import BaseEdgeMetadataV1
from grai_schemas.v1.metadata.nodes import BaseNodeMetadataV1
from grai_schemas.v1.node import NodeSpec, NodeV1, SourcedNodeSpec, SourcedNodeV1

MetadataType = Union[BaseNodeMetadataV1, BaseEdgeMetadataV1]


@merge.register
def merge_malformed_left(metadata: MalformedMetadata, other_metadata: Any) -> Metadata:
    """Merge anything into a malformed metadata object

    This handles cases where one might attempt to fix a malformed metadata object by merging a valid metadata object.

    Args:
        metadata: The malformed metadata to merge into
        other_metadata: The metadata to merge from

    Returns:
        A now valid piece of metadata
    """
    return other_metadata


@merge.register
def merge_malformed_right(metadata: Any, other_metadata: MalformedMetadata):
    """Merge a malformed metadata object into anything

    Args:
        metadata: The metadata to merge into
        other_metadata: The malformed metadata to merge from

    Raises:
        ValueError: This is always an invalid operation
    """
    raise ValueError(
        "Cannot merge malformed metadata into valid metadata. If you received this error check if any of the metadata"
        "in your objects is of type `MalformedMetadata`. This could indicate a bad value has been stored in your"
        "instance of Grai."
    )


def merge_tags(a: Optional[list], b: Optional[list]) -> list:
    """Merge two lists of tags insuring no duplicates"""
    a_tag = set(a) if a is not None else set()
    b_tag = set(b) if b is not None else set()
    return list(a_tag.union(b_tag))


@merge.register
def merge_grai_node_v1_metadata(metadata: BaseNodeMetadataV1, other_metadata: BaseNodeMetadataV1) -> BaseNodeMetadataV1:
    """Merge two grai node metadata objects

    Args:
        metadata: The node metadata to merge into
        other_metadata: The node metadata to merge from

    Returns:
        The merged node metadata
    """
    new_metadata = merge(dict(metadata), dict(other_metadata))
    new_metadata["tags"] = merge_tags(metadata.tags, other_metadata.tags)
    return BaseNodeMetadataV1(**new_metadata)


@merge.register
def merge_grai_edge_v1_metadata(metadata: BaseEdgeMetadataV1, other_metadata: BaseEdgeMetadataV1) -> BaseEdgeMetadataV1:
    """Merge two grai edge metadata objects

    Args:
        metadata: The edge metadata to merge into
        other_metadata: The edge metadata to merge from

    Returns:
        The merged edge metadata
    """
    new_metadata = merge(dict(metadata), dict(other_metadata))
    new_metadata["tags"] = merge_tags(metadata.tags, other_metadata.tags)
    return BaseEdgeMetadataV1(**new_metadata)


@merge.register
def merge_node_sourced_node(node: NodeV1, source_node: SourcedNodeV1) -> NodeV1:
    """Merge a sourced node into a node

    Args:
        node: The node to merge into
        source_node: The sourced node to merge from

    Returns:
        The merged NodeV1

    """
    new_node = node.copy()
    new_node.spec = merge(node.spec, source_node.spec)
    return new_node


@merge.register
def merge_edge_sourced_edge(edge: EdgeV1, source_edge: SourcedEdgeV1) -> EdgeV1:
    """Merge a sourced edge into an edge

    Args:
        edge: The edge to merge into
        source_edge: The sourced edge to merge from

    Returns:
        The merged EdgeV1

    """
    new_edge = edge.copy()
    new_edge.spec = merge(edge.spec, source_edge.spec)
    return new_edge


@merge.register
def merge_grai_node_into_node_metadata(spec: NodeSpec, source_spec: SourcedNodeSpec) -> NodeSpec:
    """Merge a SourcedNodeSpec into a NodeSpec

    Args:
        spec: The node spec to merge into
        source_spec: The sourced node spec to merge from

    Returns:
        The merged node spec

    """
    new_spec = copy.deepcopy(spec)
    new_spec.metadata.grai = merge(new_spec.metadata.grai, source_spec.metadata.grai)
    new_spec.metadata.sources[source_spec.data_source.name] = source_spec.metadata
    return new_spec


@merge.register
def merge_grai_edge_into_edge_metadata(spec: EdgeSpec, source_spec: SourcedEdgeSpec) -> EdgeSpec:
    """Merge grai metadata from a sourced edge into an edge spec

    Args:
        spec: The edge spec to merge into
        source_spec: The sourced edge spec to merge from

    Returns:
        The merged edge spec
    """
    new_spec = copy.deepcopy(spec)
    new_spec.metadata.grai = merge(new_spec.metadata.grai, source_spec.metadata.grai)
    new_spec.metadata.sources[source_spec.data_source.name] = source_spec.metadata
    return new_spec


@merge.register
def merge_code_into_code(code_a: Code, code_b: Code) -> Code:
    return code_b
