from typing import Dict, Type, Callable, Optional, Literal
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from uuid import UUID
from typing_extensions import Annotated
from grai_client.schemas.utilities import PlaceHolderSchema, BaseSpec, DispatchType


class BaseEdge(BaseModel):
    type: Literal["Edge"]


class EdgeNodeValues(BaseModel):
    name: str
    namespace: str

    def __hash__(self):
        return hash(hash(self.name) + hash(self.namespace))


class V1(BaseSpec):
    id: Optional[UUID]
    data_source: str
    source: Union[EdgeNodeValues, UUID]
    destination: Union[EdgeNodeValues, UUID]
    is_active: Optional[bool] = True
    metadata: Optional[Dict] = {}

    def __hash__(self):
        return hash(hash(self.source) + hash(self.destination))


class V2(PlaceHolderSchema):
    """Placeholder for future use."""
    pass


class EdgeV1(BaseEdge):
    version: Literal["v1"]
    spec: V1

    def from_spec(self, spec_dict: Dict) -> 'EdgeV1':
        args = {
            'version': self.version,
            'type': self.type,
            'spec': spec_dict,
        }
        return type(self)(**args)


class EdgeV2(BaseEdge):
    version: Literal["v2"]
    spec: V2


class EdgeType(DispatchType):
    name: str = "edges"
    type: str = 'Edge'


EdgeTypes = Union[EdgeV1, EdgeV2]
Edge = Annotated[EdgeTypes, Field(discriminator="version")]
