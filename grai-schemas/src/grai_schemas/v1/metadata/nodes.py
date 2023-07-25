from enum import Enum
from typing import Any, List, Literal, Optional, Union

from grai_schemas.generics import (
    DefaultValue,
    GraiBaseModel,
    HashableBaseModel,
    MalformedMetadata,
)
from grai_schemas.v1.metadata.generics import GenericAttributes


class NodeMetadataTypeLabels(Enum):
    """ """

    generic: Literal["Generic"] = "Generic"
    table: Literal["Table"] = "Table"
    column: Literal["Column"] = "Column"
    query: Literal["Query"] = "Query"


NodeMetadataTypeLabelLiterals = Literal["Generic", "Table", "Column", "Query"]


class SourceType(Enum):
    """ """

    database = "SQL"


class BaseNodeMetadataV1(GraiBaseModel):
    """ """

    type: Literal["NodeV1"] = "NodeV1"
    version: Literal["v1"] = "v1"
    node_type: NodeMetadataTypeLabelLiterals
    node_attributes: GenericAttributes
    tags: Optional[List[str]]


class MalformedNodeMetadataV1(MalformedMetadata, BaseNodeMetadataV1):
    """ """

    node_type: Optional[str] = "Malformed"  # type: ignore
    node_attributes: Optional[Any] = GenericAttributes()  # type: ignore


class GenericNodeMetadataV1(BaseNodeMetadataV1):
    node_type: Literal["Generic"]
    node_attributes: GenericAttributes = GenericAttributes()


class ColumnAttributes(GenericAttributes):
    """ """

    version: Literal["v1"] = "v1"
    data_type: Optional[str]  # This will need to be standardized
    default_value: Optional[DefaultValue]
    is_nullable: Optional[bool]
    is_unique: Optional[bool]
    is_primary_key: Optional[bool]


class ColumnMetadata(BaseNodeMetadataV1):
    """ """

    node_type: Literal["Column"]
    node_attributes: ColumnAttributes = ColumnAttributes()


class TableAttributes(GenericAttributes):
    """ """

    version: Literal["v1"] = "v1"


class TableMetadata(BaseNodeMetadataV1):
    """ """

    node_type: Literal["Table"]
    node_attributes: TableAttributes = TableAttributes()


class QueryAttributes(GenericAttributes):
    """ """

    version: Literal["v1"] = "v1"


class QueryMetadata(BaseNodeMetadataV1):
    """ """

    node_type: Literal["Query"]
    node_attributes: QueryAttributes = QueryAttributes()


Metadata = Union[ColumnMetadata, TableMetadata, QueryMetadata, GenericNodeMetadataV1]
