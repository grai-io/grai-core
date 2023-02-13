from typing import Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel


class V1Mixin(GraiBaseModel):
    version: Literal["v1"] = "v1"


class BaseID(GraiBaseModel):
    id: Optional[UUID]
    name: Optional[str]
    namespace: Optional[str]

    def __hash__(self):
        if self.name is None or self.namespace is None:
            raise NotImplementedError(
                f"Computing a hash for {self} requires both name and namespace for compatibility reasons."
            )
        return hash(hash(self.name) + hash(self.namespace))


class NamedID(BaseID):
    name: str
    namespace: str
    id: Optional[UUID]


class UuidID(BaseID):
    id: UUID
    name: Optional[str]
    namespace: Optional[str]


ID = Union[UuidID, NamedID]
