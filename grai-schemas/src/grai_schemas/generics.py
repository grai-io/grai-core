from typing import Any, Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.utilities import merge_dicts
from pydantic import BaseModel, root_validator


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return id(self)


class GraiBaseModel(HashableBaseModel):
    # class Config:
    #     frozen = True

    def update(self, new_values: Dict) -> BaseModel:
        values = self.dict()
        return type(self)(**merge_dicts(values, new_values))

    class Config:
        json_encoders = {UUID: lambda x: str(x)}


class PlaceHolderSchema(GraiBaseModel):
    is_active: Optional[bool] = True

    @root_validator(pre=True)
    def _(cls, values):
        message = (
            "Something is wrong... I can feel it 😡. You've reached a placeholder schema - "
            "most likely the `version` of your config file doesn't exist yet."
        )
        raise AssertionError(message)


# ----


class HasDefaultValue(GraiBaseModel):
    has_default_value: Literal[True]
    data_type: str
    default_value: Any


class NoDefaultValue(GraiBaseModel):
    has_default_value: Literal[False]
    data_type: None = None
    default_value: None = None


DefaultValue = Union[HasDefaultValue, NoDefaultValue]


# ----
