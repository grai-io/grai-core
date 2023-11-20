import abc
from typing import Annotated, Dict, Literal, Optional, Set, Union, get_args
from uuid import UUID

from grai_schemas.generics import GraiBaseModel, Metadata
from pydantic import BaseModel, Field, root_validator, validator


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

    language_name: Literal["Python"] = "Python"
    file_extension: Literal[".py"] = ".py"


class R(ProgrammingLanguage):
    """Class representation of the R programming language"""

    language_name: Literal["R"] = "R"
    file_extension: Literal[".r"] = ".r"


class SQL(ProgrammingLanguage):
    """Class representation of the SQL programming language"""

    language_name: Literal["SQL"] = "SQL"
    file_extension: Literal[".sql"] = ".sql"


class C(ProgrammingLanguage):
    """Class representation of the C programming language"""

    language_name: Literal["C"] = "C"
    file_extension: Literal[".c"] = ".c"


class CSharp(ProgrammingLanguage):
    """Class representation of the C# programming language"""

    language_name: Literal["C#"] = "C#"
    file_extension: Literal[".cs"] = ".cs"


class CPP(ProgrammingLanguage):
    """Class representation of the SQL programming language"""

    language_name: Literal["C++"] = "C++"
    file_extension: Literal[".c"] = ".c"


class Java(ProgrammingLanguage):
    """Class representation of the Java programming language"""

    language_name: Literal["Java"] = "Java"
    file_extension: Literal[".java"] = ".java"


class Scala(ProgrammingLanguage):
    """Class representation of the Scala programming language"""

    language_name: Literal["Scala"] = "Scala"
    file_extension: Literal[".scala", ".sc"] = ".scala"


class Go(ProgrammingLanguage):
    """Class representation of the Go programming language"""

    language_name: Literal["Go"] = "Go"
    file_extension: Literal[".go"] = ".go"


class JavaScript(ProgrammingLanguage):
    """Class representation of the JavaScript programming language"""

    language_name: Literal["JavaScript"] = "JavaScript"
    file_extension: Literal[".js"] = ".js"


class TypeScript(ProgrammingLanguage):
    """Class representation of the TypeScript programming language"""

    language_name: Literal["TypeScript"] = "TypeScript"
    file_extension: Literal[".ts"] = ".ts"


class Matlab(ProgrammingLanguage):
    """Class representation of the Matlab programming language"""

    language_name: Literal["Matlab"] = "Matlab"
    file_extension: Literal[".m"] = ".m"


class Swift(ProgrammingLanguage):
    """Class representation of the Swift programming language"""

    language_name: Literal["Swift"] = "Swift"
    file_extension: Literal[".swift"] = ".swift"


class Julia(ProgrammingLanguage):
    """Class representation of the Julia programming language"""

    language_name: Literal["Julia"] = "Julia"
    file_extension: Literal[".jl"] = ".jl"


class SAS(ProgrammingLanguage):
    """Class representation of the SAS programming language"""

    language_name: Literal["SAS"] = "SAS"
    file_extension: Literal[".sas"] = ".sas"


class Rust(ProgrammingLanguage):
    """Class representation of the Rust programming language"""

    language_name: Literal["Rust"] = "Rust"
    file_extension: Literal[".rs"] = ".rs"


class Perl(ProgrammingLanguage):
    """Class representation of the Perl programming language"""

    language_name: Literal["Perl"] = "Perl"
    file_extension: Literal[".pl"] = ".pl"


class Haskell(ProgrammingLanguage):
    """Class representation of the Haskell programming language"""

    language_name: Literal["Haskell"] = "Haskell"
    file_extension: Literal[".hs"] = ".hs"


class PHP(ProgrammingLanguage):
    """Class representation of the PHP programming language"""

    language_name: Literal["PHP"] = "PHP"
    file_extension: Literal[".php"] = ".php"


class Kotlin(ProgrammingLanguage):
    """Class representation of the Kotlin programming language"""

    language_name: Literal["Kotlin"] = "Kotlin"
    file_extension: Literal[".kt"] = ".kt"


class UnknownLanguage(ProgrammingLanguage):
    """Class representation of a catch-all programming language"""

    language_name: Literal["Unknown"] = "Unknown"
    original_language_name: Optional[str] = None
    file_extension: Optional[str] = None

    @root_validator(pre=True)
    def validate_malformed(cls, v: Dict):
        if v.get("language_name", "Unknown") != "Unknown":
            v["original_language_name"] = v["language_name"]
            v["language_name"] = "Unknown"
        return v


# Unknown must be last in the list as it's a catch-all
Languages = Union[
    Python,
    R,
    SQL,
    C,
    CPP,
    CSharp,
    Java,
    Scala,
    Go,
    JavaScript,
    TypeScript,
    Matlab,
    Swift,
    Julia,
    SAS,
    Rust,
    Haskell,
    Perl,
    PHP,
    Kotlin,
    UnknownLanguage,
]
LANGUAGE_LABELS: Set[str] = set()
for model in get_args(Languages):
    field_type = model.__annotations__["language_name"]
    LANGUAGE_LABELS.update(get_args(field_type))


ProgrammingLanguageTypes = Annotated[Languages, Field(discriminator="language_name")]


class Code(BaseModel):
    """A generic descriptor for Code"""

    code: Optional[str]
    has_code: bool = False
    language: ProgrammingLanguageTypes = UnknownLanguage()

    @root_validator(pre=True)
    def validate_root(cls, values):
        language = values.get("language", None)
        if isinstance(language, str):
            if language not in LANGUAGE_LABELS:
                values["language"] = {"language_name": "Unknown", "original_language_name": language}
            else:
                values["language"] = {"language_name": language}
        return values

    @validator("has_code", pre=True, always=True)
    def set_has_code(cls, value, values):
        return bool(values.get("code"))
