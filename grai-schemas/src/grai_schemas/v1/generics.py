from typing import Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel, Metadata
from pydantic import BaseModel


class BaseID(GraiBaseModel):
    """Class definition of BaseID

    Attributes:
        id: todo
        name: todo
        namespace: todo

    """

    id: Optional[UUID]
    name: Optional[str]
    namespace: Optional[str]

    def __hash__(self):
        if self.name is None or self.namespace is None:
            raise NotImplementedError(
                f"Computing a hash for {self} requires both name and namespace for compatibility reasons."
            )
        return hash((self.name, self.namespace))


class NamedID(BaseID):
    """Class definition of NamedID

    Attributes:
        id: todo
        name: todo
        namespace: todo

    """

    id: Optional[UUID]
    name: str
    namespace: str


class UuidID(BaseID):
    """Class definition of UuidID

    Attributes:
        id: todo
        name: todo
        namespace: todo

    """

    id: UUID
    name: Optional[str]
    namespace: Optional[str]


ID = Union[UuidID, NamedID]
