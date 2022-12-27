from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


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
