from typing import Union

from grai_schemas import v1
from grai_schemas.generics import GraiBaseModel, MalformedMetadata
from grai_schemas.v1.metadata import edges as edge_v1
from grai_schemas.v1.metadata import nodes as node_v1


class GraiMetadata(GraiBaseModel):
    """ """

    grai: Union[node_v1.Metadata, edge_v1.Metadata]


Node = Union[v1.node.NodeV1, v1.node.SourcedNodeV1]
Edge = Union[v1.edge.EdgeV1, v1.edge.SourcedEdgeV1]


__all__ = ["GraiMetadata"]
