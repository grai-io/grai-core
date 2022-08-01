from typing import Callable, Dict, List, Literal, Optional, Type, Union, Literal
from uuid import UUID

from grai_client.schemas.utilities import (BaseSpec,
                                           PlaceHolderSchema, GraiBaseModel)
from pydantic import Field
from typing_extensions import Annotated


class BaseEdge(GraiBaseModel):
    type: Literal["Edge"]


class EdgeNodeValues(GraiBaseModel):
    name: str
    namespace: str

    def __hash__(self):
        return hash(hash(self.name) + hash(self.namespace))


class V1(BaseSpec):
    id: Optional[UUID]
    data_source: str
    source: Union[UUID, EdgeNodeValues]
    destination: Union[UUID, EdgeNodeValues]
    is_active: Optional[bool] = True
    metadata: Optional[Dict] = {}

    def __hash__(self):
        return hash(hash(self.source) + hash(self.destination))

    def __str__(self):
        return f"Edge[Node({self.source}) -> Node({self.destination})]"


class V2(PlaceHolderSchema, V1):
    """Placeholder for future use."""

    pass


class EdgeV1(BaseEdge):
    version: Literal["v1"]
    spec: V1

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "EdgeV1":
        args = {
            "version": "v1",
            "type": "Edge",
            "spec": spec_dict,
        }
        return cls(**args)


class EdgeV2(BaseEdge):
    version: Literal["v2"]
    spec: V2

    def from_spec(self, spec_dict: Dict) -> "EdgeV2":
        raise NotImplementedError()


EdgeLabels = Literal['edge', 'edges', 'Edge', 'Edges']
EdgeTypes = Union[EdgeV1, EdgeV2]
Edge = Annotated[EdgeTypes, Field(discriminator="version")]
