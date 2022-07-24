from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_client.schemas.utilities import (BaseSpec, DispatchType,
                                           PlaceHolderSchema)
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class BaseNode(BaseModel):
    type: Literal["Node"]


class V1(BaseSpec):
    id: Optional[UUID]
    name: str
    namespace: str
    data_source: str
    display_name: Optional[str]
    is_active: Optional[bool] = True
    metadata: Optional[Dict] = {}

    def __hash__(self):
        return hash(hash(self.name) + hash(self.namespace))


class V2(PlaceHolderSchema, BaseSpec):
    pass


class NodeV1(BaseNode):
    version: Literal["v1"]
    spec: V1

    def from_spec(self, spec_dict: Dict) -> "NodeV1":
        args = {
            "version": self.version,
            "type": self.type,
            "spec": spec_dict,
        }
        return type(self)(**args)


class NodeV2(BaseNode):
    version: Literal["v2"]
    spec: V2

    def from_spec(self, spec_dict: Dict) -> "NodeV2":
        raise NotImplementedError()


class NodeType(DispatchType):
    name: str = "nodes"
    type: str = "Node"


NodeTypes = Union[NodeV1, NodeV2]
Node = Annotated[NodeTypes, Field(discriminator="version")]
