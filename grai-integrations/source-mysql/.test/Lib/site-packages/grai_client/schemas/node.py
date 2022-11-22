from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_client.schemas.utilities import (BaseSpec,
                                           PlaceHolderSchema, GraiBaseModel)
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class BaseNode(GraiBaseModel):
    type: Literal["Node"] = "Node"

    def __hash__(self):
        return


class NodeID(BaseModel):
    name: str
    namespace: str
    id: Optional[UUID]

    def __hash__(self):
        return hash(hash(self.name) + hash(self.namespace))


class V1(NodeID, BaseSpec):
    data_source: str
    display_name: Optional[str]
    is_active: Optional[bool] = True
    metadata: Optional[Dict] = {}


class V2(PlaceHolderSchema, V1):
    pass


class NodeV1(BaseNode):
    version: Literal["v1"]
    spec: V1

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "NodeV1":
        args = {
            "version": "v1",
            "type": "Node",
            "spec": spec_dict,
        }
        return cls(**args)


class NodeV2(BaseNode):
    version: Literal["v2"]
    spec: V2

    def from_spec(self, spec_dict: Dict) -> "NodeV2":
        raise NotImplementedError()


NodeLabels = Literal['nodes', 'node', 'Node', 'Nodes']
NodeTypes = Union[NodeV1, NodeV2]
Node = Annotated[NodeTypes, Field(discriminator="version")]
