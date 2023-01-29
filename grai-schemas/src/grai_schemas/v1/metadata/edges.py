from enum import Enum
from typing import Literal, Optional, Union

from grai_schemas.v1.generics import V1Mixin


class EdgeTypeLabels(Enum):
    generic = "Edge"
    table_to_column = "TableToColumn"
    column_to_column = "ColumnToColumn"


class GenericEdgeMetadataV1(V1Mixin):
    edge_type: Literal["Edge"]
    edge_attributes: dict = {}


class TableToColumnAttributes(V1Mixin):
    pass


class TableToColumnMetadata(GenericEdgeMetadataV1):
    edge_type: Literal["TableToColumn"]
    edge_attributes: TableToColumnAttributes = TableToColumnAttributes()


class ColumnToColumnAttributes(V1Mixin):
    preserves_data_type: Optional[bool] = None
    preserves_nullable: Optional[bool] = None
    preserves_unique: Optional[bool] = None


class ColumnToColumnMetadata(GenericEdgeMetadataV1):
    edge_type: Literal["ColumnToColumn"]
    edge_attributes: ColumnToColumnAttributes = ColumnToColumnAttributes()


Metadata = Union[TableToColumnMetadata, ColumnToColumnMetadata, GenericEdgeMetadataV1]
