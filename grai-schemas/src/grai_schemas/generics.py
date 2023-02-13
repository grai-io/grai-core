import abc
from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.utilities import merge_dicts
from pydantic import BaseModel, dataclasses, root_validator, validator


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
    def root_validator_of_placeholder(cls, values):
        message = (
            "Something is wrong... I can feel it 😡. You've reached a placeholder schema - "
            "most likely the `version` of your config file doesn't exist yet."
        )
        raise AssertionError(message)


# ----


class DefaultValue(GraiBaseModel):
    has_default_value: Optional[bool] = None
    data_type: Optional[str] = None
    default_value: Optional[Any] = None

    @root_validator()
    def validate_default_value_root(cls, values):
        if isinstance(values, dict):
            has_default_value = values.get("has_default_value", None)
            data_type = values.get("data_type", None)
            default_value = values.get("default_value", None)
        # elif isinstance(values, DefaultValue):
        #     breakpoint()
        #     has_default_value = values.has_default_value
        #     data_type = values.data_type
        #     default_value = values.default_value
        else:
            raise NotImplementedError(f"No available implementation to produce a DefaultValue from a {type(values)}")

        if has_default_value is None or has_default_value is False:
            assert data_type is None, "Cannot set a data_type when `has_default_value` is not True"
            assert default_value is None, "Cannot set a default_value when `has_default_value` is not True"
        else:
            assert data_type is not None, "If `has_default_value` is True, a `data_type` is required"
            assert default_value is not None, "If `has_default_value` is True, a `default_value` is required"

        return values


# ----


class PackageConfig(BaseModel):
    integration_name: str
    metadata_id: str

    @validator("metadata_id")
    def metadata_id_validation(cls, value):
        assert (
            "-" not in value
        ), f"Error found in metadata_id: {value}. `-` is a reserved character which should not be used."
        return value

    class Config:
        validate_assignment = True
        validate_all = True
