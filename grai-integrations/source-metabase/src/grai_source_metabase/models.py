from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from grai_source_metabase import api


class MetabaseModelDefaults(BaseModel):
    namespace: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Question(MetabaseModelDefaults, api.Question):
    @property
    def full_name(self):
        return f"Question: {self.name}.{self.id}"


class Column(MetabaseModelDefaults, api.TableMetadataField):
    table_id: int
    table_schema: str
    table_name: str

    def full_name(self):
        return f"{self.table_schema}.{self.table_name}.{self.name}"


class TableMetadata(MetabaseModelDefaults, api.TableMetadata):
    def get_columns(self) -> List[Column]:
        table_kwargs = {
            "table_name": self.name,
            "table_schema": self.table_schema,
            "namespace": self.namespace,
            "table_id": self.id,
        }
        columns = [Column(**field.dict(), **table_kwargs) for field in self.fields]
        return columns

    def get_edges(self) -> List["Edge"]:
        base_kwargs = {"namespace": self.namespace}
        edges = [Edge() for field in self.fields]


class Table(MetabaseModelDefaults, api.Table):
    @property
    def full_name(self):
        return f"{self.table_schema}.{self.name}"


class Collection(MetabaseModelDefaults, api.Collection):
    @property
    def full_name(self):
        return f"Collection: {self.name}"


NodeTypes = Union[Question, Table, Collection, Column]


class Edge(BaseModel):
    source: NodeTypes
    destination: NodeTypes
    definition: Optional[str]
    metadata: Optional[Dict] = None
    namespace: str

    def __hash__(self):
        return hash((self.source, self.destination))
