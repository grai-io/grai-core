from typing import Literal, Optional

from grai_schemas.generics import GraiBaseModel, HashableBaseModel
from grai_schemas.v1.generics import V1Mixin
from pydantic import root_validator


class GenericAttributes(HashableBaseModel):
    class Config:
        """ """

        extra = "allow"
        allow_mutation = True
