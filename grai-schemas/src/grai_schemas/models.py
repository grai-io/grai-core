from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel


class NodeTypes(Enum):
    table = "Table"
    column = "Column"


class SourceType(Enum):
    database = "SQL"


class DefaultValue(BaseModel):
    has_default_value: bool
    data_type: Optional[str]
    default_value: Optional[Any]


class ColumnAttributes(BaseModel):
    data_type: str  # This will need to be standardized
    default_value: DefaultValue = DefaultValue(has_default_value=False)
    is_nullable: Optional[bool]
    is_primary_key: Optional[bool]


class TableAttributes(BaseModel):
    pass


class GraiNodeMetadata(BaseModel):
    version: Literal["v1"] = "v1"
    node_type: NodeTypes
    node_attributes: Any


class Column(GraiNodeMetadata):
    node_type: Literal["Column"] = "Column"
    node_attributes: ColumnAttributes


class Table(GraiNodeMetadata):
    node_type: Literal["Table"] = "Table"
    node_attributes: TableAttributes
