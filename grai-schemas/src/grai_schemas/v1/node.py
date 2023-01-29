from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.generics import ID, BaseID, NamedID, UuidID
from grai_schemas.v1.metadata.metadata import MetadataV1
from grai_schemas.v1.metadata.nodes import GenericNodeMetadataV1


class NodeNamedID(NamedID):
    pass


class NodeUuidID(UuidID):
    pass


NodeIdTypes = Union[NodeUuidID, NodeNamedID]


class BaseSpec(GraiBaseModel):
    is_active: Optional[bool] = True
    data_source: str
    display_name: Optional[str]
    workspace: Optional[UUID]
    metadata: MetadataV1 = MetadataV1(grai=GenericNodeMetadataV1(node_type="Node"))


class NamedSpec(NodeNamedID, BaseSpec):
    pass


class IDSpec(NodeUuidID, BaseSpec):
    pass


NodeSpec = Union[IDSpec, NamedSpec]


class NodeV1(GraiBaseModel):
    type: Literal["Node"]
    version: Literal["v1"]
    spec: NodeSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "NodeV1":
        return cls(version="v1", type="Node", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)
