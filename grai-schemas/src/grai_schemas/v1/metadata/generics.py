from grai_schemas.generics import HashableBaseModel


class GenericAttributes(HashableBaseModel):
    class Config:
        """ """

        extra = "allow"
        allow_mutation = True
