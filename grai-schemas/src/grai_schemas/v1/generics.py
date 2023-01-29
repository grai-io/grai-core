from typing import Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel


class V1Mixin(GraiBaseModel):
    version: Literal["v1"] = "v1"


class BaseID(GraiBaseModel):
    id: Optional[UUID]
    name: Optional[str]
    namespace: Optional[str]


class NamedID(BaseID):
    name: str
    namespace: str
    id: Optional[UUID]

    def __hash__(self):
        return hash(hash(self.name) + hash(self.namespace))


class UuidID(BaseID):
    id: UUID
    name: Optional[str]
    namespace: Optional[str]

    def __hash__(self):
        return hash(self.id)


ID = Union[UuidID, NamedID]
