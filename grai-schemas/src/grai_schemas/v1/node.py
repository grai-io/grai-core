from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.generics import ID, BaseID, NamedID, UuidID
from grai_schemas.v1.metadata.metadata import (
    GraiMetadataV1,
    GraiNodeMetadataV1,
    MetadataV1,
    NodeMetadataV1,
)
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
    metadata: GraiNodeMetadataV1 = GraiNodeMetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"))

    @validator("metadata", always=True, pre=True)
    def validate_metadata(cls, v: Optional[Union[Dict, GraiNodeMetadataV1]]) -> GraiNodeMetadataV1:
        if isinstance(v, GraiNodeMetadataV1):
            return v
        elif isinstance(v, dict):
            v.setdefault("grai", GenericNodeMetadataV1(node_type="Generic"))
            return GraiNodeMetadataV1(**v)
        elif v is None:
            return GraiNodeMetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"))
        raise ValueError(f"Invalid metadata: {v}. Expected either None, a dict, or a MetadataV1 instance.")


class NamedSourceSpec(NodeNamedID, BaseSpec, SourcedNodeSpecMetadataMixin, DataSourceMixin):
    """ """

    def to_node(self) -> "NamedSpec":
        """

        Returns:

        """
        values = self.dict(exclude={"metadata", "data_source"})
        values["data_sources"] = [self.data_source]
        values["metadata"] = {"grai": self.metadata.grai, "sources": {self.data_source.name: self.metadata}}
        return NamedSpec(**values)


class IDSourceSpec(NodeUuidID, BaseSpec, SourcedNodeSpecMetadataMixin, DataSourceMixin):
    """ """

    def to_node(self) -> "IDSpec":
        """

        Returns:

        """
        values = self.dict()
        values["data_sources"] = [values.pop("data_source")]
        values["metadata"] = {
            "grai": values["metadata"]["grai"],
            "sources": {self.data_source.name: values["metadata"]},
        }
        return IDSpec(**values)


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

    def to_node(self) -> "NodeV1":
        """

        Returns:

        """
        return NodeV1(version="v1", type="Node", spec=self.spec.to_node())


class NodeSpecMetadataMixin(GraiBaseModel):
    metadata: NodeMetadataV1 = NodeMetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"), sources={})

    @validator("metadata", always=True, pre=True)
    def validate_metadata(cls, v: Optional[Union[Dict, NodeMetadataV1]]) -> NodeMetadataV1:
        if isinstance(v, NodeMetadataV1):
            return v
        elif isinstance(v, dict):
            v.setdefault("grai", GenericNodeMetadataV1(node_type="Generic"))
            v.setdefault("sources", {})
            return NodeMetadataV1(**v)
        elif v is None:
            return NodeMetadataV1(grai=GenericNodeMetadataV1(node_type="Generic"), sources={})
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
