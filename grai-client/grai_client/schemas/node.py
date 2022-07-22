from typing import Optional, Union, Dict, Literal
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from uuid import UUID
from grai_client.schemas.utilities import PlaceHolderSchema, BaseGraiType


class V1(BaseModel):
    id: Optional[UUID]
    name: str
    namespace: str
    data_source: str
    display_name: Optional[str]
    is_active: Optional[bool] = True
    metadata: Optional[Dict] = {}

    def __hash__(self):
        return hash(hash(self.name) + hash(self.namespace))


class V2(PlaceHolderSchema):
    pass


class NodeV1(BaseModel):
    version: Literal["v1"]
    type: Literal["Node"]
    spec: V1

    def from_spec(self, spec_dict: Dict):
        args = {
            'version': self.version,
            'type': self.type,
            'spec': spec_dict,
        }
        return type(self)(**args)


class NodeV2(BaseModel):
    version: Literal["v2"]
    type: Literal["Node"]
    spec: V2


Node = Annotated[Union[NodeV1, NodeV2], Field(discriminator="version")]


class NodeType(BaseGraiType):
    name = "nodes"
    type = "Node"
