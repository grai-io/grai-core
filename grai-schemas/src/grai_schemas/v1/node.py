from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.generics import ID, BaseID, NamedID, UuidID
from grai_schemas.v1.metadata.metadata import MetadataV1
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
    metadata: MetadataV1 = MetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"))

    @validator("metadata", always=True, pre=True)
    def validate_metadata(cls, v: Optional[Union[Dict, MetadataV1]]) -> MetadataV1:
        if isinstance(v, MetadataV1):
            return v
        elif isinstance(v, dict):
            v.setdefault("grai", GenericNodeMetadataV1(node_type="Generic"))
            return MetadataV1(**v)
        elif v is None:
            return MetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"))
        raise ValueError(f"Invalid metadata: {v}. Expected either None, a dict, or a MetadataV1 instance.")


class NamedSourceSpec(NodeNamedID, BaseSpec, DataSourceMixin):
    """ """

    pass


class IDSourceSpec(NodeUuidID, BaseSpec, DataSourceMixin):
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


class NamedSpec(NodeNamedID, BaseSpec, DataSourcesMixin):
    """ """

    pass


class IDSpec(NodeUuidID, BaseSpec, DataSourcesMixin):
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
