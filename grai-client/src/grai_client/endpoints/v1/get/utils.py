from typing import Any, Dict, TypeVar

from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.metadata.metadata import (
    GraiMalformedEdgeMetadataV1,
    GraiMalformedNodeMetadataV1,
)

from grai_client.endpoints.utilities import handles_bad_metadata

T = TypeVar("T")


@handles_bad_metadata(GraiMalformedNodeMetadataV1)
def node_builder(resp: Dict[str, Any]) -> NodeV1:
    return NodeV1.from_spec(resp)


@handles_bad_metadata(GraiMalformedNodeMetadataV1)
def source_node_builder(resp: Dict[str, Any]) -> SourcedNodeV1:
    return SourcedNodeV1.from_spec(resp)


@handles_bad_metadata(GraiMalformedEdgeMetadataV1)
def edge_builder(resp: Dict[str, Any]) -> EdgeV1:
    return EdgeV1.from_spec(resp)


@handles_bad_metadata(GraiMalformedEdgeMetadataV1)
def source_edge_builder(resp: Dict[str, Any]) -> SourcedEdgeV1:
    return SourcedEdgeV1.from_spec(resp)
