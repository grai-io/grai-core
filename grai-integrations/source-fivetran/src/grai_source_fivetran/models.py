from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator

from grai_source_fivetran.fivetran_api.api_models import (
    ColumnMetadataResponse,
    SchemaMetadataResponse,
    TableMetadataResponse,
)


class TableResult(BaseModel):
    id: str
    name_in_source: str
    parent_id: str
    name_in_destination: str


class ColumnResult(BaseModel):
    id: str
    name_in_source: str
    type_in_source: str
    is_foreign_key: bool
    is_primary_key: bool
    name_in_destination: str
    type_in_destination: str
    parent_id: str


class SchemaResult(BaseModel):
    id: str
    name_in_source: str
    name_in_destination: str


class DestinationConfig(BaseModel):
    host: str
    port: int
    database: str
    auth: str
    user: str
    password: str


class DestinationMetadata(BaseModel):
    id: str  # e.x. decent_dropsy
    group_id: str  # e.x. decent_dropsy
    service: str  # e.x. snowflake
    region: str  # e.x. GCP_US_EAST4
    time_zone_offset: int  # e.x. -5
    setup_status: str  # e.x. connected
    config: DestinationConfig


class ConnectorTablePatchSettings(BaseModel):
    allowed: bool
    reason: str
    reason_code: str


class ConnectorTableColumnSchema(BaseModel):
    name_in_destination: str
    enabled: bool
    hashed: bool
    enabled_patch_settings: ConnectorTablePatchSettings


class ConnectorTableSchema(BaseModel):
    sync_mode: str
    name_in_destination: str
    enabled: bool
    enabled_patch_settings: ConnectorTablePatchSettings
    columns: Dict[str, ConnectorTableColumnSchema]


class ConnectorSchema(BaseModel):
    name_in_destination: str
    enabled: bool
    tables: Dict[str, ConnectorTableSchema]


class ConnectorMetadata(BaseModel):
    enable_new_by_default: bool
    schema_change_handling: str
    schemas: Dict[str, ConnectorSchema]


class SourceTableColumnMetadata(BaseModel):
    columns: Dict[str, ConnectorTableColumnSchema]


class NamespaceIdentifier(BaseModel):
    source: str
    destination: str


class Column(BaseModel):
    name: str
    namespace: str
    fivetran_id: str
    fivetran_table_id: str
    table_name: str
    table_schema: str
    is_primary_key: bool
    is_foreign_key: bool

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.table_name}.{self.name}"

    @classmethod
    def from_fivetran_models(
        cls,
        schema: SchemaMetadataResponse,
        table: TableMetadataResponse,
        column: ColumnMetadataResponse,
        namespace: NamespaceIdentifier,
    ):
        source_values = {
            "name": column.name_in_source,
            "fivetran_id": column.id,
            "fivetran_table_id": column.parent_id,
            "is_primary_key": column.is_primary_key,
            "is_foreign_key": column.is_foreign_key,
            "table_name": table.name_in_source,
            "table_schema": schema.name_in_source,
            "namespace": namespace.source,
        }
        destination_values = {
            "name": column.name_in_destination,
            "fivetran_id": column.id,
            "fivetran_table_id": column.parent_id,
            "is_primary_key": column.is_primary_key,
            "is_foreign_key": column.is_foreign_key,
            "table_name": table.name_in_destination,
            "table_schema": schema.name_in_destination,
            "namespace": namespace.destination,
        }
        return cls(**source_values), cls(**destination_values)


class Table(BaseModel):
    name: str
    namespace: str
    fivetran_id: str
    schema_name: str

    @property
    def full_name(self):
        return f"{self.schema_name}.{self.name}"

    @classmethod
    def from_fivetran_models(
        cls,
        schema: SchemaMetadataResponse,
        table: TableMetadataResponse,
        namespace: NamespaceIdentifier,
    ):
        source_values = {
            "name": table.name_in_source,
            "schema_name": schema.name_in_source,
            "fivetran_id": table.id,
            "namespace": namespace.source,
        }
        destination_values = {
            "name": table.name_in_destination,
            "schema_name": schema.name_in_destination,
            "fivetran_id": table.id,
            "namespace": namespace.destination,
        }
        return cls(**source_values), cls(**destination_values)


class Constraint(str, Enum):
    belongs_to = "bt"
    copy = "c"


NodeTypes = Union[Column, Table]


class Edge(BaseModel):
    source: NodeTypes
    destination: NodeTypes
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None

    def __hash__(self):
        return hash((self.source, self.destination))
