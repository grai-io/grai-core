from enum import Enum
from typing import Any, Literal, Optional, Union

from grai_schemas.generics import DefaultValue, HashableBaseModel
from grai_schemas.v1.generics import GraiBaseModel, V1Mixin


class NodeTypeLabels(Enum):
    generic = "Node"
    table = "Table"
    column = "Column"


class SourceType(Enum):
    database = "SQL"


class GenericNodeMetadataV1(V1Mixin):
    node_type: Literal["Node"]
    node_attributes: dict = {}


class ColumnAttributes(GraiBaseModel):
    data_type: Optional[str]  # This will need to be standardized
    default_value: Optional[DefaultValue]
    is_nullable: Optional[bool]
    is_unique: Optional[bool]
    is_primary_key: Optional[bool]


class ColumnMetadata(GenericNodeMetadataV1):
    node_type: Literal["Column"]
    node_attributes: ColumnAttributes = ColumnAttributes()


class TableAttributes(HashableBaseModel):
    pass


class TableMetadata(GenericNodeMetadataV1):
    node_type: Literal["Table"]
    node_attributes: TableAttributes = TableAttributes()


Metadata = Union[ColumnMetadata, TableMetadata, GenericNodeMetadataV1]
