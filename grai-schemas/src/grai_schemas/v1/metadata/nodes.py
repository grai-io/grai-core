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
        generic: The literal "Generic
        table: The literal "Table"
        column: The literal "Column"
        query: The literal "Query"
        collection: The literal "Collection"

    """

    generic: Literal["Generic"] = "Generic"
    table: Literal["Table"] = "Table"
    column: Literal["Column"] = "Column"
    query: Literal["Query"] = "Query"
    collection: Literal["Collection"] = "Collection"


NodeMetadataTypeLabelLiterals = Literal["Generic", "Table", "Column", "Query", "Collection"]


class SourceType(Enum):
    """Class definition of SourceType

    Attributes:
        database: todo

    """

    database: Literal["SQL"] = "SQL"


class BaseNodeMetadataV1(GraiBaseModel):
    """Class definition of BaseNodeMetadataV1

    Attributes:
        type: Object type of the Metadata e.g. NodeV1, EdgeV1, etc.
        version: Schema version of the metadata
        node_type: The type of node e.g. Table, Column, etc.
        node_attributes: Attributes specific to the node type
        tags: Tags associated with the node

    """

    type: Literal["NodeV1"] = "NodeV1"
    version: Literal["v1"] = "v1"
    node_type: NodeMetadataTypeLabelLiterals
    node_attributes: GenericAttributes
    tags: Optional[List[str]]


class MalformedNodeMetadataV1(MalformedMetadata, BaseNodeMetadataV1):
    """Class definition of MalformedNodeMetadataV1

    Attributes:
        node_type: The literal "Malformed"
        node_attributes: Attributes specific to the node type

    """

    node_type: Optional[str] = "Malformed"  # type: ignore
    node_attributes: Optional[Any] = GenericAttributes()  # type: ignore


class GenericNodeMetadataV1(BaseNodeMetadataV1):
    """Class definition of GenericNodeMetadataV1

    Attributes:
        node_type: The literal "Generic"
        node_attributes: Attributes specific to the node type

    """

    node_type: Literal["Generic"]
    node_attributes: GenericAttributes = GenericAttributes()


class ColumnAttributes(GenericAttributes):
    """Class definition of ColumnAttributes

    Attributes:
        version: Schema version of the metadata
        data_type: The data type of the column
        default_value: The default value of the column
        is_nullable: Whether values in the column is nullable
        is_unique: Whether values in the column are unique
        is_primary_key: Whether the column is a primary key

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
        node_type: The type of node e.g. Table, Column, etc.
        node_attributes: Attributes specific to the node type

    """

    node_type: Literal["Column"]
    node_attributes: ColumnAttributes = ColumnAttributes()


class TableAttributes(GenericAttributes):
    """Class definition of TableAttributes

    Attributes:
        version: Schema version of the metadata

    """

    version: Literal["v1"] = "v1"


class TableMetadata(BaseNodeMetadataV1):
    """Class definition of TableMetadata

    Attributes:
        node_type: The type of node e.g. Table, Column, etc.
        node_attributes: Attributes specific to the node type

    """

    node_type: Literal["Table"]
    node_attributes: TableAttributes = TableAttributes()


class QueryAttributes(GenericAttributes):
    """Class definition of QueryAttributes

    Attributes:
        version: Schema version of the metadata

    """

    version: Literal["v1"] = "v1"


class QueryMetadata(BaseNodeMetadataV1):
    """Class definition of QueryMetadata

    Attributes:
        node_type: The type of node e.g. Table, Column, etc.
        node_attributes: Attributes specific to the node type

    """

    node_type: Literal["Query"]
    node_attributes: QueryAttributes = QueryAttributes()


class CollectionMetadata(BaseNodeMetadataV1):
    """Class definition of CollectionMetadata

    Attributes:
        node_type: The type of node e.g. Table, Column, etc.
        node_attributes: Attributes specific to the node type

    """

    node_type: Literal["Collection"]
    node_attributes: GenericAttributes = GenericAttributes()


Metadata = Union[ColumnMetadata, TableMetadata, QueryMetadata, CollectionMetadata, GenericNodeMetadataV1]
