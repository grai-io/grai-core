from typing import Callable, Dict, List, Literal, Optional, Type, Union
from uuid import UUID

from grai_schemas.v1.generics import GraiBaseModel, NamedID, UuidID
from grai_schemas.v1.metadata.edges import GenericEdgeMetadataV1, Metadata
from grai_schemas.v1.metadata.metadata import EdgeMetadataV1, GraiEdgeMetadataV1
from grai_schemas.v1.node import NodeIdTypes
from grai_schemas.v1.source import DataSourceMixin, DataSourcesMixin
from pydantic import validator


class EdgeNamedID(NamedID):
    """ """

    pass


class EdgeUuidID(UuidID):
    """ """

    pass


EdgeIdTypes = Union[EdgeUuidID, EdgeNamedID]


class BaseSpec(GraiBaseModel):
    """ """

    display_name: Optional[str]
    source: NodeIdTypes
    destination: NodeIdTypes
    is_active: Optional[bool] = True
    workspace: Optional[UUID]

    def __str__(self):
        return f"Edge[Node({self.source}) -> Node({self.destination})]"


class SourcedEdgeSpecMetadataMixin(GraiBaseModel):
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


class NamedSourceSpec(EdgeNamedID, BaseSpec, SourcedEdgeSpecMetadataMixin, DataSourceMixin):
    """ """

    pass

    def to_edge(self) -> "NamedSpec":
        """

        Returns:

        """
        values = self.dict(exclude={"data_source", "metadata"})
        values["data_sources"] = [self.data_source]
        values["metadata"] = {
            "grai": self.metadata.grai,
            "sources": {self.data_source.name: self.metadata},
        }
        return NamedSpec(**values)


class IDSourceSpec(EdgeUuidID, BaseSpec, SourcedEdgeSpecMetadataMixin, DataSourceMixin):
    """ """

    pass

    def to_edge(self) -> "IDSpec":
        """

        Returns:

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
    type: Literal["SourceEdge"]
    version: Literal["v1"]
    spec: SourcedEdgeSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "SourcedEdgeV1":
        """

        Args:
            spec_dict (Dict):

        Returns:

        Raises:

        """
        return cls(version="v1", type="SourceEdge", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)

    def to_edge(self) -> "EdgeV1":
        return EdgeV1(version="v1", type="Edge", spec=self.spec.to_edge())


class EdgeSpecMetadataMixin(GraiBaseModel):
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


class NamedSpec(EdgeNamedID, BaseSpec, EdgeSpecMetadataMixin, DataSourcesMixin):
    """ """

    pass


class IDSpec(EdgeUuidID, BaseSpec, EdgeSpecMetadataMixin, DataSourcesMixin):
    """ """

    pass


EdgeSpec = Union[IDSpec, NamedSpec]


class EdgeV1(GraiBaseModel):
    """ """

    type: Literal["Edge"]
    version: Literal["v1"]
    spec: EdgeSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "EdgeV1":
        """

        Args:
            spec_dict (Dict):

        Returns:

        Raises:

        """
        return cls(version="v1", type="Edge", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)
