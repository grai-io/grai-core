import copy
from typing import Any, Dict, Optional, Union

from grai_schemas.generics import MalformedMetadata, Metadata
from grai_schemas.utilities import merge
from grai_schemas.v1.edge import EdgeSpec, EdgeV1, SourcedEdgeSpec, SourcedEdgeV1
from grai_schemas.v1.metadata.edges import BaseEdgeMetadataV1
from grai_schemas.v1.metadata.nodes import BaseNodeMetadataV1
from grai_schemas.v1.node import NodeSpec, NodeV1, SourcedNodeSpec, SourcedNodeV1

MetadataType = Union[BaseNodeMetadataV1, BaseEdgeMetadataV1]


@merge.register
def merge_malformed_left(metadata: MalformedMetadata, other_metadata: Any) -> Metadata:
    """ """
    return other_metadata


@merge.register
def merge_malformed_right(metadata: Any, other_metadata: MalformedMetadata):
    """ """
    raise ValueError(
        "Cannot merge malformed metadata into valid metadata. If you received this error check if any of the metadata"
        "in your objects is of type `MalformedMetadata`. This could indicate a bad value has been stored in your"
        "instance of Grai."
    )


def merge_tags(a: Optional[list], b: Optional[list]) -> list:
    a_tag = set(a) if a is not None else set()
    b_tag = set(b) if b is not None else set()
    return list(a_tag.union(b_tag))


@merge.register
def merge_grai_node_v1_metadata(metadata: BaseNodeMetadataV1, other_metadata: BaseNodeMetadataV1) -> BaseNodeMetadataV1:
    """ """
    new_metadata = merge(dict(metadata), dict(other_metadata))
    new_metadata["tags"] = merge_tags(metadata.tags, other_metadata.tags)
    return BaseNodeMetadataV1(**new_metadata)


@merge.register
def merge_grai_edge_v1_metadata(metadata: BaseEdgeMetadataV1, other_metadata: BaseEdgeMetadataV1) -> BaseEdgeMetadataV1:
    """ """
    new_metadata = merge(dict(metadata), dict(other_metadata))
    new_metadata["tags"] = merge_tags(metadata.tags, other_metadata.tags)
    return BaseEdgeMetadataV1(**new_metadata)


@merge.register
def merge_node_sourced_node(node: NodeV1, source_node: SourcedNodeV1) -> NodeV1:
    """ """
    new_node = node.copy()
    new_node.spec = merge(node.spec, source_node.spec)
    return new_node


@merge.register
def merge_edge_sourced_edge(edge: EdgeV1, source_edge: SourcedEdgeV1) -> EdgeV1:
    """ """
    new_edge = edge.copy()
    new_edge.spec = merge(edge.spec, source_edge.spec)
    return new_edge


@merge.register
def merge_grai_node_into_node_metadata(spec: NodeSpec, source_spec: SourcedNodeSpec) -> NodeSpec:
    """ """
    new_spec = copy.deepcopy(spec)
    new_spec.metadata.grai = merge(new_spec.metadata.grai, source_spec.metadata.grai)
    new_spec.metadata.sources[source_spec.data_source.name] = source_spec.metadata
    return new_spec


@merge.register
def merge_grai_edge_into_edge_metadata(spec: EdgeSpec, source_spec: SourcedEdgeSpec) -> NodeSpec:
    """ """
    new_spec = copy.deepcopy(spec)
    new_spec.metadata.grai = merge(new_spec.metadata.grai, source_spec.metadata.grai)
    new_spec.metadata.sources[source_spec.data_source.name] = source_spec.metadata
    return new_spec
