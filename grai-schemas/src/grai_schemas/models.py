import uuid
from enum import Enum
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, Field


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


class V1(HashableBaseModel):
    version: Literal["v1"] = "v1"


class ColumnAttributes(HashableBaseModel):
    data_type: Optional[str]  # This will need to be standardized
    default_value: Optional[DefaultValue]
    is_nullable: Optional[bool]
    is_unique: Optional[bool]
    is_primary_key: Optional[bool]


class ColumnMetadata(V1):
    node_type: Literal["Column"] = "Column"
    node_attributes: ColumnAttributes = ColumnAttributes()


class TableAttributes(HashableBaseModel):
    pass


class TableMetadata(V1):
    node_type: Literal["Table"] = "Table"
    node_attributes: TableAttributes = TableAttributes()


GraiNodeMetadata = Annotated[
    Union[ColumnMetadata, TableMetadata], Field(discriminator="node_type")
]


class TableToColumnAttributes(V1):
    pass


class TableToColumnMetadata(V1):
    edge_type: Literal["TableToColumn"] = "TableToColumn"
    edge_attributes: TableToColumnAttributes = TableToColumnAttributes()


class ColumnToColumnAttributes(V1):
    preserves_data_type: Optional[bool] = None
    preserves_nullable: Optional[bool] = None
    preserves_unique: Optional[bool] = None


class ColumnToColumnMetadata(V1):
    edge_type: Literal["TableToColumn"] = "ColumnToColumn"
    edge_attributes: ColumnToColumnAttributes = ColumnToColumnAttributes()


GraiEdgeMetadata = Annotated[
    Union[TableToColumnMetadata, ColumnToColumnMetadata],
    Field(discriminator="edge_type"),
]
