from typing import Union

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.metadata import edges, nodes


class GraiMetadataV1(GraiBaseModel):
    grai: Union[edges.Metadata, nodes.Metadata]


class MetadataV1(GraiMetadataV1):
    class Config:
        extra = "allow"
