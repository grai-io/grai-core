from typing import Any, Dict, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel, MalformedMetadata, Metadata
from grai_schemas.utilities import merge
from grai_schemas.v1.metadata import edges, nodes


class GraiNodeMetadataV1(Metadata):
    """ """

    grai: nodes.Metadata


class GraiEdgeMetadataV1(Metadata):
    """ """

    grai: edges.Metadata


GraiMetadataV1 = Union[GraiNodeMetadataV1, GraiEdgeMetadataV1]


class SourcesNodeMetadataV1(Metadata):
    """"""

    sources: Dict[str, GraiNodeMetadataV1]


class SourcesEdgeMetadataV1(Metadata):
    """"""

    sources: Dict[str, GraiEdgeMetadataV1]


SourcesMetadataV1 = Union[SourcesNodeMetadataV1, SourcesEdgeMetadataV1]


class NodeMetadataV1(GraiNodeMetadataV1, SourcesNodeMetadataV1):
    """ """

    pass


class EdgeMetadataV1(GraiEdgeMetadataV1, SourcesEdgeMetadataV1):
    """ """

    pass


MetadataV1 = Union[NodeMetadataV1, EdgeMetadataV1]


class GraiMalformedNodeMetadataV1(MalformedMetadata, NodeMetadataV1):
    """ """

    grai: nodes.MalformedNodeMetadataV1 = nodes.MalformedNodeMetadataV1()  # type: ignore
    sources: Dict[str, nodes.Metadata] = {}


class GraiMalformedEdgeMetadataV1(MalformedMetadata, EdgeMetadataV1):
    """ """

    grai: edges.MalformedEdgeMetadataV1 = edges.MalformedEdgeMetadataV1()  # type: ignore
    sources: Dict[str, edges.Metadata] = {}
