from typing import Callable, Dict, List, Literal, Optional, Type, Union
from uuid import UUID

from grai_schemas.v1.generics import GraiBaseModel, NamedID, UuidID
from grai_schemas.v1.metadata.edges import GenericEdgeMetadataV1, Metadata
from grai_schemas.v1.metadata.metadata import EdgeMetadataV1, GraiEdgeMetadataV1
from grai_schemas.v1.node import NodeIdTypes
from grai_schemas.v1.source import DataSourceMixin, DataSourcesMixin, SourceSpec
from pydantic import validator


class EdgeNamedID(NamedID):
    """Class definition of EdgeNamedID"""

    pass


class EdgeUuidID(UuidID):
    """Class definition of EdgeUuidID"""

    pass


EdgeIdTypes = Union[EdgeUuidID, EdgeNamedID]


class BaseSourcedEdgeSpec(GraiBaseModel):
    """Class definition of BaseSourcedEdgeSpec

    Attributes:
        display_name: An optional short form name for the edge
        source: The source node of the edge
        destination: The destination node of the edge
        is_active: Whether the edge is active or not
        workspace: The workspace the edge belongs to
        data_source: The data source which created this edge
        metadata: Metadata associated with the edge.

    """

    display_name: Optional[str]
    source: NodeIdTypes
    destination: NodeIdTypes
    is_active: Optional[bool] = True
    workspace: Optional[UUID]
    data_source: SourceSpec
    metadata: GraiEdgeMetadataV1 = GraiEdgeMetadataV1(grai=GenericEdgeMetadataV1(edge_type="Generic"))

    @validator("metadata", always=True, pre=True)
    def validate_metadata(cls, v: Optional[Union[Dict, GraiEdgeMetadataV1]]) -> GraiEdgeMetadataV1:
        if isinstance(v, GraiEdgeMetadataV1):
            return v
        elif isinstance(v, dict):
            v.setdefault("grai", GenericEdgeMetadataV1(edge_type="Generic"))
            return GraiEdgeMetadataV1(**v)
        elif v is None:
            return GraiEdgeMetadataV1(grai=GenericEdgeMetadataV1(edge_type="Generic"))
        raise ValueError(f"Invalid metadata: {v}. Expected either None, a dict, or a MetadataV1 instance.")

    def __str__(self) -> str:
        return f"Edge[Node({self.source}) -> Node({self.destination})]"


class NamedSourceSpec(EdgeNamedID, BaseSourcedEdgeSpec):
    """Class definition of NamedSourceSpec"""

    def to_edge(self) -> "NamedSpec":
        """

        Returns:
            A NamedSpec instance
        """
        values = self.dict(exclude={"data_source", "metadata"})
        values["data_sources"] = [self.data_source]
        values["metadata"] = {
            "grai": self.metadata.grai,
            "sources": {self.data_source.name: self.metadata},
        }
        return NamedSpec(**values)


class IDSourceSpec(EdgeUuidID, BaseSourcedEdgeSpec):
    """Class definition of IDSourceSpec"""

    def to_edge(self) -> "IDSpec":
        """

        Returns:
            An IDSpec instance
        """
        values = self.dict(exclude={"data_source", "metadata"})
        values["data_sources"] = [self.data_source]
        values["metadata"] = {
            "grai": self.metadata.grai,
            "sources": {self.data_source.name: self.metadata},
        }
        return IDSpec(**values)


SourcedEdgeSpec = Union[IDSourceSpec, NamedSourceSpec]


class SourcedEdgeV1(GraiBaseModel):
    """Class definition of SourcedEdgeV1

    Attributes:
        type: The type of the edge e.g. NodeV1, EdgeV1, etc...
        version: Object version e.g. v1
        spec: The edge specification

    """

    type: Literal["SourceEdge"]
    version: Literal["v1"]
    spec: SourcedEdgeSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "SourcedEdgeV1":
        """

        Args:
            spec_dict (Dict):

        Returns:
            A SourcedEdgeV1 instance

        Raises:

        """
        return cls(version="v1", type="SourceEdge", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)

    def to_edge(self) -> "EdgeV1":
        """Converts a SourcedEdgeV1 instance to an EdgeV1 instance

        Returns:
            An EdgeV1 instance
        """
        return EdgeV1(version="v1", type="Edge", spec=self.spec.to_edge())


class BaseEdgeSpec(GraiBaseModel):
    """Class definition of BaseEdgeSpec

    Attributes:
        display_name: An optional short form name for the edge
        source: The source node of the edge
        destination: The destination node of the edge
        is_active: Whether the edge is active or not
        workspace: The workspace the edge belongs to
        data_sources: The data sources which have contributed to this edge
        metadata: Metadata associated with the edge.

    """

    display_name: Optional[str]
    source: NodeIdTypes
    destination: NodeIdTypes
    is_active: Optional[bool] = True
    workspace: Optional[UUID]
    data_sources: List[Union[UUID, SourceSpec]]
    metadata: EdgeMetadataV1 = EdgeMetadataV1(grai=GenericEdgeMetadataV1(edge_type="Generic"), sources={})

    @validator("metadata", always=True, pre=True)
    def validate_metadata(cls, v: Optional[Union[Dict, EdgeMetadataV1]]) -> EdgeMetadataV1:
        if isinstance(v, EdgeMetadataV1):
            return v
        elif isinstance(v, dict):
            v.setdefault("grai", GenericEdgeMetadataV1(edge_type="Generic"))
            v.setdefault("sources", {})
            return EdgeMetadataV1(**v)
        elif v is None:
            return EdgeMetadataV1(grai=GenericEdgeMetadataV1(edge_type="Generic"), sources={})
        raise ValueError(f"Invalid metadata: {v}. Expected either None, a dict, or a MetadataV1 instance.")

    def __str__(self):
        return f"Edge[Node({self.source}) -> Node({self.destination})]"


class NamedSpec(EdgeNamedID, BaseEdgeSpec):
    """Class definition of NamedSpec"""

    pass


class IDSpec(EdgeUuidID, BaseEdgeSpec):
    """Class definition of IDSpec"""

    pass


EdgeSpec = Union[IDSpec, NamedSpec]


class EdgeV1(GraiBaseModel):
    """Class definition of EdgeV1

    Attributes:
        type: The type of the edge e.g. NodeV1, EdgeV1, etc...
        version: Object version e.g. v1
        spec: The edge specification

    """

    type: Literal["Edge"]
    version: Literal["v1"]
    spec: EdgeSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "EdgeV1":
        """

        Args:
            spec_dict (Dict):

        Returns:
            An EdgeV1 instance

        Raises:

        """
        return cls(version="v1", type="Edge", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)
