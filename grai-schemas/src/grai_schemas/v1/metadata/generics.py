from typing import Literal, Optional

from grai_schemas import generics


class GenericAttributes(generics.HashableBaseModel):
    """Class definition of GenericAttributes"""

    class Config:
        """ """

        extra = "allow"
        allow_mutation = True
