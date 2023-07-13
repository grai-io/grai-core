from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.generics import ID, BaseID, NamedID, UuidID
from grai_schemas.v1.metadata.metadata import GraiMetadataV1, MetadataV1
from grai_schemas.v1.metadata.nodes import GenericNodeMetadataV1
from grai_schemas.v1.source import DataSourceMixin, DataSourcesMixin
from pydantic import Field, validator


class NodeNamedID(NamedID):
    """ """

    pass


class NodeUuidID(UuidID):
    """ """

    pass


NodeIdTypes = Union[NodeUuidID, NodeNamedID]


class BaseSpec(GraiBaseModel):
    """ """

    is_active: Optional[bool] = True
    display_name: Optional[str]
    workspace: Optional[UUID]


class SourcedNodeSpecMetadataMixin(GraiBaseModel):
    metadata: GraiMetadataV1 = GraiMetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"))

    @validator("metadata", always=True, pre=True)
    def validate_metadata(cls, v: Optional[Union[Dict, GraiMetadataV1]]) -> GraiMetadataV1:
        if isinstance(v, GraiMetadataV1):
            return v
        elif isinstance(v, dict):
            v.setdefault("grai", GenericNodeMetadataV1(node_type="Generic"))
            return GraiMetadataV1(**v)
        elif v is None:
            return GraiMetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"))
        raise ValueError(f"Invalid metadata: {v}. Expected either None, a dict, or a MetadataV1 instance.")


class NamedSourceSpec(NodeNamedID, BaseSpec, SourcedNodeSpecMetadataMixin, DataSourceMixin):
    """ """

    pass


class IDSourceSpec(NodeUuidID, BaseSpec, SourcedNodeSpecMetadataMixin, DataSourceMixin):
    """ """

    pass


SourcedNodeSpec = Union[IDSourceSpec, NamedSourceSpec]


class SourcedNodeV1(GraiBaseModel):
    type: Literal["SourceNode"]
    version: Literal["v1"]
    spec: SourcedNodeSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "SourcedNodeV1":
        """

        Args:
            spec_dict (Dict):

        Returns:

        Raises:

        """
        return cls(version="v1", type="SourceNode", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)


class NodeSpecMetadataMixin(GraiBaseModel):
    metadata: MetadataV1 = MetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"), sources={})

    @validator("metadata", always=True, pre=True)
    def validate_metadata(cls, v: Optional[Union[Dict, MetadataV1]]) -> MetadataV1:
        if isinstance(v, MetadataV1):
            return v
        elif isinstance(v, dict):
            v.setdefault("grai", GenericNodeMetadataV1(node_type="Generic"))
            v.setdefault("sources", {})
            return MetadataV1(**v)
        elif v is None:
            return MetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"), sources={})
        raise ValueError(f"Invalid metadata: {v}. Expected either None, a dict, or a MetadataV1 instance.")


class NamedSpec(NodeNamedID, BaseSpec, NodeSpecMetadataMixin, DataSourcesMixin):
    """ """

    pass


class IDSpec(NodeUuidID, BaseSpec, NodeSpecMetadataMixin, DataSourcesMixin):
    """ """

    pass


NodeSpec = Union[IDSpec, NamedSpec]


class NodeV1(GraiBaseModel):
    """ """

    type: Literal["Node"]
    version: Literal["v1"]
    spec: NodeSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "NodeV1":
        """

        Args:
            spec_dict (Dict):

        Returns:

        Raises:

        """
        return cls(version="v1", type="Node", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)


# __all__ = ["NodeSpec", "NodeV1", "SourcedNodeSpec", "SourcedNodeV1", "NodeIdTypes", "NodeNamedID", "NodeUuidID", "BaseSpec", "NamedSourceSpec", "IDSourceSpec"]
