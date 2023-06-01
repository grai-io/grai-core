from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from grai_schemas.v1.generics import V1Mixin
from grai_schemas.v1.metadata.generics import GenericAttributes


class EdgeTypeLabels(Enum):
    """ """

    generic = "Generic"
    table_to_column = "TableToColumn"
    column_to_column = "ColumnToColumn"
    table_to_table = "TableToTable"


EdgeTypeLabelLiterals = Literal["Generic", "TableToColumn", "ColumnToColumn", "TableToTable"]


class BaseEdgeMetadataV1(V1Mixin):
    """ """

    type: Literal["EdgeV1"] = "EdgeV1"
    edge_type: EdgeTypeLabelLiterals
    edge_attributes: GenericAttributes
    tags: Optional[List[str]]


class GenericEdgeMetadataV1(BaseEdgeMetadataV1):
    edge_type: Literal["Generic"]
    edge_attributes: GenericAttributes = GenericAttributes()


class TableToColumnAttributes(GenericAttributes):
    """ """

    pass


class TableToColumnMetadata(BaseEdgeMetadataV1):
    """ """

    edge_type: Literal["TableToColumn"]
    edge_attributes: TableToColumnAttributes = TableToColumnAttributes()


class TableToTableAttributes(GenericAttributes):
    """ """

    pass


class TableToTableMetadata(BaseEdgeMetadataV1):
    """ """

    edge_type: Literal["TableToTable"]
    edge_attributes: TableToTableAttributes = TableToTableAttributes()


class ColumnToColumnAttributes(GenericAttributes):
    """ """

    preserves_data_type: Optional[bool] = None
    preserves_nullable: Optional[bool] = None
    preserves_unique: Optional[bool] = None


class ColumnToColumnMetadata(BaseEdgeMetadataV1):
    """ """

    edge_type: Literal["ColumnToColumn"]
    edge_attributes: ColumnToColumnAttributes = ColumnToColumnAttributes()


Metadata = Union[TableToColumnMetadata, TableToTableMetadata, ColumnToColumnMetadata, GenericEdgeMetadataV1]
