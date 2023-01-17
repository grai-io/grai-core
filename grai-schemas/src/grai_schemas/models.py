import uuid
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return id(self)


class NodeTypes(Enum):
    table = "Table"
    column = "Column"


class SourceType(Enum):
    database = "SQL"


class DefaultValue(HashableBaseModel):
    has_default_value: bool
    data_type: Optional[str]
    default_value: Optional[Any]


class ColumnAttributes(HashableBaseModel):
    data_type: Optional[str]  # This will need to be standardized
    default_value: Optional[DefaultValue]
    is_nullable: Optional[bool]
    is_unique: Optional[bool]
    is_primary_key: Optional[bool]


class TableAttributes(HashableBaseModel):
    pass


class GraiNodeMetadata(HashableBaseModel):
    version: Literal["v1"] = "v1"
    node_type: NodeTypes
    node_attributes: Any


class ColumnMetadata(GraiNodeMetadata):
    node_type: Literal["Column"] = "Column"
    node_attributes: ColumnAttributes = ColumnAttributes()


class TableMetadata(GraiNodeMetadata):
    node_type: Literal["Table"] = "Table"
    node_attributes: TableAttributes = TableAttributes()


class EdgeAttributes(HashableBaseModel):
    pass


class TableToColumnAttributes(EdgeAttributes):
    pass


class ColumnToColumnAttributes(EdgeAttributes):
    preserves_data_type: Optional[bool] = None
    preserves_nullable: Optional[bool] = None
    preserves_unique: Optional[bool] = None


class GraiEdgeMetadata(HashableBaseModel):
    version: Literal["v1"] = "v1"
    edge_attributes: EdgeAttributes = EdgeAttributes()
