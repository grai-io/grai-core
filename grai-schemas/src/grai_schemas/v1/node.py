from typing import Dict, List, Literal, Optional, Union
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
from grai_schemas.v1.source import SourceSpec
from pydantic import Field, validator


class NodeNamedID(NamedID):
    """ """

    pass


class NodeUuidID(UuidID):
    """ """

    pass


NodeIdTypes = Union[NodeUuidID, NodeNamedID]


class BaseSourcedNodeSpec(GraiBaseModel):
    """Class definition of BaseSourcedNodeSpec

    Attributes:
        is_active: whether the node is active or not
        display_name: An optional short form name for the node
        workspace: The workspace the node belongs to
        metadata: Metadata associated with the node.
    """

    is_active: Optional[bool] = True
    display_name: Optional[str]
    workspace: Optional[UUID]
    data_source: SourceSpec
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


class NamedSourceSpec(NodeNamedID, BaseSourcedNodeSpec):
    """Class definition of NamedSourceSpec"""

    def to_node(self) -> "NamedSpec":
        """

        Returns:

        """
        values = self.dict(exclude={"metadata", "data_source"})
        values["data_sources"] = [self.data_source]
        values["metadata"] = {"grai": self.metadata.grai, "sources": {self.data_source.name: self.metadata}}
        return NamedSpec(**values)


class IDSourceSpec(NodeUuidID, BaseSourcedNodeSpec):
    """Class definition of IDSourceSpec"""

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
    """Class definition of SourcedNodeV1

    Attributes:
        type: The type of the object e.g. Node, Edge, etc.
        version: The version of the object e.g. v1
        spec: The sourced node specification.

    """

    type: Literal["SourceNode"]
    version: Literal["v1"]
    spec: SourcedNodeSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "SourcedNodeV1":
        """

        Args:
            spec_dict:

        Returns:

        Raises:

        """
        return cls(version="v1", type="SourceNode", spec=spec_dict)

    def __hash__(self):
        """Custom hash for SourcedNodeV1"""
        return hash(self.spec)

    def to_node(self) -> "NodeV1":
        """Convert a SourcedNodeV1 to a NodeV1

        Returns:

        """
        return NodeV1(version="v1", type="Node", spec=self.spec.to_node())


class BaseNodeSpec(GraiBaseModel):
    """Class definition of BaseSpec

    Attributes:
        is_active: whether the node is active or not
        display_name: An optional short form name for the node
        workspace: The workspace the node belongs to
        data_sources: The data sources which created this object.
        metadata: Metadata associated with the node.

    """

    is_active: Optional[bool] = True
    display_name: Optional[str]
    workspace: Optional[UUID]
    data_sources: List[Union[UUID, SourceSpec]]
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


class NamedSpec(NodeNamedID, BaseNodeSpec):
    """ """

    pass


class IDSpec(NodeUuidID, BaseNodeSpec):
    """ """

    pass


NodeSpec = Union[IDSpec, NamedSpec]


class NodeV1(GraiBaseModel):
    """Class definition of NodeV1

    Attributes:
        type: todo
        version: todo
        spec: todo

    """

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
