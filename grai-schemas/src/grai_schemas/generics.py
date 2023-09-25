from typing import Any, Dict, Literal, Optional, TypeVar, Union
from uuid import UUID

from grai_schemas.serializers import dump_json, load_json
from grai_schemas.utilities import merge
from pydantic import BaseModel, dataclasses, root_validator, validator

T = TypeVar("T")


class HashableBaseModel(BaseModel):
    """A BaseModel that is hashable"""

    def __hash__(self):
        return id(self)


class GraiBaseModel(HashableBaseModel):
    """The base class for all Grai models

    This class provides a number of features which are useful for Grai models:
    * hashable - this allows Grai models to be used as keys in dictionaries
    * update - this allows Grai models to be updated with new values
    * json_loads - this allows Grai models to be loaded from JSON
    * json_dumps - this allows Grai models to be dumped to JSON

    In addition there is are pydantic specific configuration changes which enforce consistent behavior across Grai Models:
    * validate_all - this ensures that all fields are validated
    * validate_assignment - this ensures that all fields are validated when assigned
    * allow_population_by_field_name - this allows Grai models to be updated with new values by field name
    * orm_mode - this allows Grai models to be used with ORMs

    """

    # class Config:
    #     frozen = True

    def update(self, new_values: Dict) -> BaseModel:
        """Automatically update a Grai model with new values

        Update uses the `merge` function to update the current model with new values.
        Merge understands the nested structure of Grai models and will update nested models correctly.

        Args:
            new_values (Dict):

        Returns:
            An updated instance of the current model

        Raises:

        """
        values = self.dict()
        return type(self)(**merge(values, new_values))

    class Config:
        """ """

        json_loads = load_json
        json_dumps = dump_json
        # json_encoders = {UUID: lambda x: str(x)}
        validate_all = True
        validate_assignment = True
        allow_population_by_field_name = True
        orm_mode = True


class PlaceHolderSchema(GraiBaseModel):
    """Class definition of PlaceHolderSchema

    This is a placeholder schema which is used when a schema version is not yet available.
    It should not be used for any other purpose.

    Attributes:
        is_active: todo

    """

    is_active: Optional[bool] = True

    @root_validator(pre=True)
    def root_validator_of_placeholder(cls, values):
        """

        Args:
            values:

        Returns:

        Raises:

        """
        message = (
            "Something is wrong... I can feel it 😡. You've reached a placeholder schema - "
            "most likely the `version` of your config file doesn't exist yet."
        )
        raise AssertionError(message)


# ----


class DefaultValue(GraiBaseModel):
    """Class definition of DefaultValue

    Attributes:
        has_default_value: Identifies whether a default value is available
        data_type: The data type of the default value
        default_value: The default value

    """

    has_default_value: Optional[bool] = None
    data_type: Optional[str] = None
    default_value: Optional[Any] = None

    @root_validator()
    def validate_default_value_root(cls, values):
        """

        Args:
            values:

        Returns:

        Raises:

        """
        if isinstance(values, dict):
            has_default_value = values.get("has_default_value", None)
            data_type = values.get("data_type", None)
            default_value = values.get("default_value", None)
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
    """Class definition of PackageConfig

    Attributes:
        integration_name: todo
        metadata_id: todo

    """

    integration_name: str
    metadata_id: str

    @validator("metadata_id")
    def metadata_id_validation(cls, value):
        """

        Args:
            value:

        Returns:

        Raises:

        """
        assert (
            "-" not in value
        ), f"Error found in metadata_id: {value}. `-` is a reserved character which should not be used."
        return value

    class Config:
        """ """

        validate_assignment = True
        validate_all = True


class Metadata(GraiBaseModel):
    """A base class for all metadata models"""

    pass

    class Config:
        """ """

        extra = "allow"
        allow_mutation = True


class MalformedMetadata(GraiBaseModel):
    """Class definition of MalformedMetadata

    Attributes:
        malformed_values: A cache of values used to instantiate the class.

    """

    malformed_values: Dict = {}

    @root_validator(pre=True)
    def validate_malformed(cls, v):
        """ """
        return {"malformed_values": {**v}}

    def dict(self, *args, **kwargs):
        """ """
        return self.malformed_values
