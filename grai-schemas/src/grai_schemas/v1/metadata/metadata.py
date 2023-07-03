from typing import Any, Optional, Union

from grai_schemas.generics import GraiBaseModel, MalformedMetadata, Metadata
from grai_schemas.utilities import merge
from grai_schemas.v1.metadata import edges, nodes


class GraiMetadataV1(Metadata):
    """ """

    grai: Union[edges.Metadata, nodes.Metadata]


class MetadataV1(GraiMetadataV1):
    """ """

    class Config:
        """ """

        extra = "allow"
        allow_mutation = True


class GraiMalformedNodeMetadataV1(MalformedMetadata, MetadataV1):
    """ """

    grai: nodes.MalformedNodeMetadataV1 = nodes.MalformedNodeMetadataV1()  # type: ignore


class GraiMalformedEdgeMetadataV1(MalformedMetadata, MetadataV1):
    """ """

    grai: edges.MalformedEdgeMetadataV1 = edges.MalformedEdgeMetadataV1()  # type: ignore
