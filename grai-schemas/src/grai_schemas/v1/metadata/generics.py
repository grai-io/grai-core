from typing import Literal, Optional

from grai_schemas.generics import GraiBaseModel, HashableBaseModel


class GenericAttributes(HashableBaseModel):
    class Config:
        """ """

        extra = "allow"
        allow_mutation = True
