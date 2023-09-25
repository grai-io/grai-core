from typing import Any, Dict, Optional, Union
from uuid import UUID

from grai_schemas.generics import MalformedMetadata, Metadata
from grai_schemas.utilities import merge
from grai_schemas.v1.metadata import edges, nodes


class GraiNodeMetadataV1(Metadata):
    """Class definition of GraiNodeMetadataV1

    Attributes:
        grai: Grai defined operation attributes

    """

    grai: nodes.Metadata


class GraiEdgeMetadataV1(Metadata):
    """Class definition of GraiEdgeMetadataV1

    Attributes:
        grai: Grai defined operation attributes

    """

    grai: edges.Metadata


GraiMetadataV1 = Union[GraiNodeMetadataV1, GraiEdgeMetadataV1]


class SourcesNodeMetadataV1(Metadata):
    """Class definition of SourcesNodeMetadataV1

    Attributes:
        sources: A dictionary of source names to source metadata

    """

    sources: Dict[str, GraiNodeMetadataV1]


class SourcesEdgeMetadataV1(Metadata):
    """Class definition of SourcesEdgeMetadataV1

    Attributes:
        sources: A dictionary of source names to source metadata

    """

    sources: Dict[str, GraiEdgeMetadataV1]


SourcesMetadataV1 = Union[SourcesNodeMetadataV1, SourcesEdgeMetadataV1]


class NodeMetadataV1(GraiNodeMetadataV1, SourcesNodeMetadataV1):
    """Class definition of NodeMetadataV1"""

    pass


class EdgeMetadataV1(GraiEdgeMetadataV1, SourcesEdgeMetadataV1):
    """Class definition of EdgeMetadataV1"""

    pass


MetadataV1 = Union[NodeMetadataV1, EdgeMetadataV1]


class GraiMalformedNodeMetadataV1(MalformedMetadata, NodeMetadataV1):
    """Class definition of GraiMalformedNodeMetadataV1

    Attributes:
        grai: Grai defined operation attributes
        sources: A dictionary of source names to source metadata

    """

    grai: nodes.MalformedNodeMetadataV1 = nodes.MalformedNodeMetadataV1()  # type: ignore
    sources: Dict[str, nodes.Metadata] = {}


class GraiMalformedEdgeMetadataV1(MalformedMetadata, EdgeMetadataV1):
    """Class definition of GraiMalformedEdgeMetadataV1

    Attributes:
        grai: Grai defined operation attributes
        sources: A dictionary of source names to source metadata

    """

    grai: edges.MalformedEdgeMetadataV1 = edges.MalformedEdgeMetadataV1()  # type: ignore
    sources: Dict[str, edges.Metadata] = {}
