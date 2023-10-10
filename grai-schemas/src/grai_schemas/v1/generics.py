import abc
from typing import Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel, Metadata
from pydantic import BaseModel, validator


class BaseID(GraiBaseModel):
    """Class definition of BaseID

    Attributes:
        id: Optional UUID of the object
        name: Optional name of the object
        namespace: Optional namespace of the object

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
        id: Optional UUID of the object
        name: Name of the object
        namespace: Namespace of the object

    """

    id: Optional[UUID]
    name: str
    namespace: str


class UuidID(BaseID):
    """Class definition of UuidID

    Attributes:
        id: UUID of the object
        name: Optional name of the object
        namespace: Optional namespace of the object

    """

    id: UUID
    name: Optional[str]
    namespace: Optional[str]


ID = Union[UuidID, NamedID]


class ProgrammingLanguage(BaseModel):
    pass


class Python(ProgrammingLanguage):
    """Class representation of the Python programming language"""

    language_name: Literal["Python"]
    file_extension: Literal[".py"] = ".py"


class R(ProgrammingLanguage):
    """Class representation of the R programming language"""

    language_name: Literal["R"]
    file_extension: Literal[".r"] = ".r"


class SQL(ProgrammingLanguage):
    """Class representation of the SQL programming language"""

    language_name: Literal["SQL"]
    file_extension: Literal[".sql"] = ".sql"


class UnknownLanguage(ProgrammingLanguage):
    """Class representation catch-all programming language"""

    language_name: str = "Unknown"
    file_extension: Optional[str] = None


ProgrammingLanguage = Union[Python, R, SQL, UnknownLanguage]


class Code(BaseModel):
    """A generic descriptor for Code"""

    code: Optional[str]
    has_code: bool = False
    language: ProgrammingLanguage = UnknownLanguage()

    @validator("has_code", pre=True, always=True)
    def set_has_code(cls, value, values):
        return bool(values.get("code"))
