from typing import Any, Dict, Tuple, TypeVar, Union

from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.edge import EdgeSpec, SourcedEdgeSpec
from grai_schemas.v1.metadata.metadata import (
    GraiMalformedEdgeMetadataV1,
    GraiMalformedNodeMetadataV1,
)
from grai_schemas.v1.node import NodeSpec, SourcedNodeSpec
from grai_schemas.v1.source import SourceSpec

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get_is_unique
from grai_client.endpoints.utilities import handles_bad_metadata
from grai_client.endpoints.v1.client import ClientV1

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


def get_source_and_spec(
    client: ClientV1, grai_type: Union[SourcedNodeSpec, SourcedEdgeSpec]
) -> Tuple[SourceSpec, Union[NodeSpec, EdgeSpec]]:
    source = grai_type.data_source
    if source.id is None:
        source = get_is_unique(client, source).spec

    if isinstance(grai_type, SourcedEdgeSpec):
        label = "Edge"
    elif isinstance(grai_type, SourcedNodeSpec):
        label = "Node"
    else:
        raise ValueError(f"Unexpected type: {type(grai_type)}")

    if (obj := grai_type).id is None:
        sub_options = ClientOptions(query_args={"name": grai_type.name, "namespace": grai_type.namespace})
        obj = get_is_unique(client, label, sub_options).spec

    return source, obj
