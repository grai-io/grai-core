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
    """Class definition of NodeMetadataTypeLabels

    Attributes:
        generic: todo
        table: todo
        column: todo
        query: todo
        collection: todo

    """

    generic: Literal["Generic"] = "Generic"
    table: Literal["Table"] = "Table"
    column: Literal["Column"] = "Column"
    query: Literal["Query"] = "Query"
    collection: Literal["Collection"] = "Collection"


NodeMetadataTypeLabelLiterals = Literal["Generic", "Table", "Column", "Query", "Collection"]


class SourceType(Enum):
    """ """

    database = "SQL"


class BaseNodeMetadataV1(GraiBaseModel):
    """Class definition of BaseNodeMetadataV1

    Attributes:
        type: todo
        version: todo
        node_type: todo
        node_attributes: todo
        tags: todo

    """

    type: Literal["NodeV1"] = "NodeV1"
    version: Literal["v1"] = "v1"
    node_type: NodeMetadataTypeLabelLiterals
    node_attributes: GenericAttributes
    tags: Optional[List[str]]


class MalformedNodeMetadataV1(MalformedMetadata, BaseNodeMetadataV1):
    """Class definition of MalformedNodeMetadataV1

    Attributes:
        node_type: todo
        node_attributes: todo

    """

    node_type: Optional[str] = "Malformed"  # type: ignore
    node_attributes: Optional[Any] = GenericAttributes()  # type: ignore


class GenericNodeMetadataV1(BaseNodeMetadataV1):
    """Class definition of GenericNodeMetadataV1

    Attributes:
        node_type: todo
        node_attributes: todo

    """

    node_type: Literal["Generic"]
    node_attributes: GenericAttributes = GenericAttributes()


class ColumnAttributes(GenericAttributes):
    """Class definition of ColumnAttributes

    Attributes:
        version: todo
        data_type: todo
        default_value: todo
        is_nullable: todo
        is_unique: todo
        is_primary_key: todo

    """

    version: Literal["v1"] = "v1"
    data_type: Optional[str]  # This will need to be standardized
    default_value: Optional[DefaultValue]
    is_nullable: Optional[bool]
    is_unique: Optional[bool]
    is_primary_key: Optional[bool]


class ColumnMetadata(BaseNodeMetadataV1):
    """Class definition of ColumnMetadata

    Attributes:
        node_type: todo
        node_attributes: todo

    """

    node_type: Literal["Column"]
    node_attributes: ColumnAttributes = ColumnAttributes()


class TableAttributes(GenericAttributes):
    """Class definition of TableAttributes

    Attributes:
        version: todo

    """

    version: Literal["v1"] = "v1"


class TableMetadata(BaseNodeMetadataV1):
    """Class definition of TableMetadata

    Attributes:
        node_type: todo
        node_attributes: todo

    """

    node_type: Literal["Table"]
    node_attributes: TableAttributes = TableAttributes()


class QueryAttributes(GenericAttributes):
    """Class definition of QueryAttributes

    Attributes:
        version: todo

    """

    version: Literal["v1"] = "v1"


class QueryMetadata(BaseNodeMetadataV1):
    """Class definition of QueryMetadata

    Attributes:
        node_type: todo
        node_attributes: todo

    """

    node_type: Literal["Query"]
    node_attributes: QueryAttributes = QueryAttributes()


class CollectionMetadata(BaseNodeMetadataV1):
    """Class definition of CollectionMetadata

    Attributes:
        node_type: todo
        node_attributes: todo

    """

    node_type: Literal["Collection"]
    node_attributes: GenericAttributes = GenericAttributes()


Metadata = Union[ColumnMetadata, TableMetadata, QueryMetadata, CollectionMetadata, GenericNodeMetadataV1]
