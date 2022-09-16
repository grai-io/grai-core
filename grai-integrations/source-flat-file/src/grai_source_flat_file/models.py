from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


class ID(BaseModel):
    name: str
    namespace: str
    full_name: str


class TableID(ID):
    table_schema: str

    @root_validator(pre=True)
    def make_full_name(cls, values):
        full_name = values.get("full_name", None)
        if values.get("full_name", None) is None:
            values["full_name"] = f"{values['table_schema']}.{values['name']}"
        return values


class ColumnID(ID):
    table_schema: str
    table_name: str

    @root_validator(pre=True)
    def make_full_name(cls, values):
        full_name = values.get("full_name", None)
        if values.get("full_name", None) is None:
            values[
                "full_name"
            ] = f"{values['table_schema']}.{values['table_name']}.{values['name']}"
        return values


class Column(BaseModel):
    name: str = Field(alias="column_name")
    namespace: str
    table: str
    data_type: str
    is_nullable: bool
    full_name: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

    @validator("full_name", always=True)
    def make_full_name(cls, full_name, values):
        if full_name is not None:
            return full_name
        result = f"{values['table']}.{values['name']}"
        return result


