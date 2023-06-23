from typing import Callable, Dict, List, Literal, Optional, Type, Union
from uuid import UUID

from grai_schemas.v1.generics import GraiBaseModel, NamedID, UuidID
from grai_schemas.v1.metadata.edges import GenericEdgeMetadataV1, Metadata
from grai_schemas.v1.metadata.metadata import MetadataV1
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
    metadata: MetadataV1 = MetadataV1(grai=GenericEdgeMetadataV1(edge_type="Generic"))

    def __str__(self):
        return f"Edge[Node({self.source}) -> Node({self.destination})]"

    @validator("metadata", always=True, pre=True)
    def validate_metadata(cls, v: Optional[Union[Dict, MetadataV1]]) -> MetadataV1:
        if isinstance(v, MetadataV1):
            return v
        elif isinstance(v, dict):
            v.setdefault("grai", GenericEdgeMetadataV1(edge_type="Generic"))
            return MetadataV1(**v)
        elif v is None:
            return MetadataV1(grai=GenericEdgeMetadataV1(edge_type="Generic"))
        raise ValueError(f"Invalid metadata: {v}. Expected either None, a dict, or a MetadataV1 instance.")


class NamedSourceSpec(EdgeNamedID, BaseSpec, DataSourceMixin):
    """ """

    pass


class IDSourceSpec(EdgeUuidID, BaseSpec, DataSourceMixin):
    """ """

    pass


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


class NamedSpec(EdgeNamedID, BaseSpec, DataSourcesMixin):
    """ """

    pass


class IDSpec(EdgeUuidID, BaseSpec, DataSourcesMixin):
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
