from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from grai_schemas.generics import GraiBaseModel, MalformedMetadata
from grai_schemas.v1.metadata.generics import GenericAttributes


class EdgeMetadataTypeLabels(Enum):
    """ """

    generic = "Generic"
    table_to_column = "TableToColumn"
    column_to_column = "ColumnToColumn"
    table_to_table = "TableToTable"


EdgeTypeLabelLiterals = Literal["Generic", "TableToColumn", "ColumnToColumn", "TableToTable"]


class BaseEdgeMetadataV1(GraiBaseModel):
    """Class definition of BaseEdgeMetadataV1

    Attributes:
        type: todo
        version: todo
        edge_type: todo
        edge_attributes: todo
        tags: todo

    """

    type: Literal["EdgeV1"] = "EdgeV1"
    version: Literal["v1"] = "v1"
    edge_type: EdgeTypeLabelLiterals
    edge_attributes: GenericAttributes
    tags: Optional[List[str]]


class MalformedEdgeMetadataV1(MalformedMetadata, BaseEdgeMetadataV1):
    """Class definition of MalformedEdgeMetadataV1

    Attributes:
        edge_type: todo
        edge_attributes: todo

    """

    edge_type: Optional[str] = "Malformed"  # type: ignore
    edge_attributes: Optional[Any] = GenericAttributes()  # type: ignore


class GenericEdgeMetadataV1(BaseEdgeMetadataV1):
    """Class definition of GenericEdgeMetadataV1

    Attributes:
        edge_type: todo
        edge_attributes: todo

    """

    edge_type: Literal["Generic"]
    edge_attributes: GenericAttributes = GenericAttributes()


class TableToColumnAttributes(GenericAttributes):
    """Class definition of TableToColumnAttributes

    Attributes:
        version: todo

    """

    version: Literal["v1"] = "v1"
    pass


class TableToColumnMetadata(BaseEdgeMetadataV1):
    """Class definition of TableToColumnMetadata

    Attributes:
        edge_type: todo
        edge_attributes: todo

    """

    edge_type: Literal["TableToColumn"]
    edge_attributes: TableToColumnAttributes = TableToColumnAttributes()


class TableToTableAttributes(GenericAttributes):
    """Class definition of TableToTableAttributes

    Attributes:
        version: todo

    """

    version: Literal["v1"] = "v1"
    pass


class TableToTableMetadata(BaseEdgeMetadataV1):
    """Class definition of TableToTableMetadata

    Attributes:
        edge_type: todo
        edge_attributes: todo

    """

    edge_type: Literal["TableToTable"]
    edge_attributes: TableToTableAttributes = TableToTableAttributes()


class ColumnToColumnAttributes(GenericAttributes):
    """Class definition of ColumnToColumnAttributes

    Attributes:
        version: todo
        preserves_data_type: todo
        preserves_nullable: todo
        preserves_unique: todo

    """

    version: Literal["v1"] = "v1"
    preserves_data_type: Optional[bool] = None
    preserves_nullable: Optional[bool] = None
    preserves_unique: Optional[bool] = None


class ColumnToColumnMetadata(BaseEdgeMetadataV1):
    """Class definition of ColumnToColumnMetadata

    Attributes:
        edge_type: todo
        edge_attributes: todo

    """

    edge_type: Literal["ColumnToColumn"]
    edge_attributes: ColumnToColumnAttributes = ColumnToColumnAttributes()


Metadata = Union[TableToColumnMetadata, TableToTableMetadata, ColumnToColumnMetadata, GenericEdgeMetadataV1]
