from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, PrivateAttr


class MetabaseDbmsVersion(BaseModel):
    flavor: str
    semantic_version: Optional[List]
    version: str


class DB(BaseModel):
    dbms_version: Optional[MetabaseDbmsVersion]
    engine: Optional[str]
    id: int
    name: str
    timezone: Optional[str]


class QuestionResultMetadata(BaseModel):
    # id: int
    base_type: str
    description: Optional[str]
    fingerprint: Optional[Dict]
    display_name: Optional[str]


class QuestionDataSetQuery(BaseModel):
    database: int
    query: Optional[Dict]
    type: str


class Question(BaseModel):
    id: int
    name: str
    table_id: Optional[int]
    database_id: Optional[int]
    collection_id: Optional[int]
    description: Optional[str]
    archived: Optional[bool]
    result_metadata: Optional[List[QuestionResultMetadata]]
    dataset_query: Optional[QuestionDataSetQuery]
    # ---- unvalidated ----#
    creator: Optional[Dict]
    public_uuid: Optional[str]
    collection: Optional[Dict]


class TableDB(BaseModel):
    id: int
    name: str
    dbms_version: Optional[MetabaseDbmsVersion]
    engine: str


class Table(BaseModel):
    id: int
    name: str
    active: Optional[bool]
    display_name: Optional[str]
    table_schema: str = Field(alias="schema")
    entity_type: Optional[str]
    db_id: int
    description: Optional[str]
    db: TableDB


class FingerPrintGlobal(BaseModel):
    distinct_count: int = Field(..., alias="distinct-count")
    null_percent: float = Field(..., alias="nil%")

    class Config:
        allow_population_by_field_name = True


class FingerPrint(BaseModel):
    global_stats: Optional[FingerPrintGlobal] = Field(alias="global")
    type_stats: Optional[Dict] = Field(alias="type")


class TableMetadataField(BaseModel):
    id: int
    name: str
    display_name: str
    active: bool
    description: Optional[str]
    fingerprint: Optional[FingerPrint]


class TableMetadata(BaseModel):
    id: int
    name: str
    table_schema: str = Field(..., alias="schema")
    active: bool
    db: Optional[TableDB]
    db_id: int
    display_name: str
    fields: Optional[List[TableMetadataField]]


class Collection(BaseModel):
    name: str
    id: int
    parent_id: Optional[str]
    archived: Optional[bool]

    @property
    def full_name(self):
        return f"Collection: {self.name}"
