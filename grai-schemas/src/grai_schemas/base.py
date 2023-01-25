from typing import Union

from grai_schemas import v1
from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.metadata import edges as edge_v1
from grai_schemas.v1.metadata import nodes as node_v1


class GraiMetadata(GraiBaseModel):
    grai: Union[node_v1.Metadata, edge_v1.Metadata]


Node = v1.node.NodeV1
Edge = v1.edge.EdgeV1
