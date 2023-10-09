from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel

from grai_source_metabase import api


class MetabaseModelDefaults(BaseModel):
    namespace: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Question(MetabaseModelDefaults, api.Question):
    obj_type: Literal["Question"] = "Question"

    @property
    def full_name(self):
        return f"Question: {self.name}.{self.id}"


class Column(MetabaseModelDefaults, api.TableMetadataField):
    obj_type: Literal["Column"] = "Column"
    db_id: int
    table_id: int
    table_schema: str
    table_name: str

    def __hash__(self):
        return hash((self.db_id, self.full_name))

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.table_name}.{self.name}"


class TableMetadata(MetabaseModelDefaults, api.TableMetadata):
    def get_columns(self) -> List[Column]:
        table_kwargs = {
            "table_name": self.name,
            "table_schema": self.table_schema,
            "namespace": self.namespace,
            "table_id": self.id,
            "db_id": self.db_id,
        }
        if self.fields is None:
            return []
        columns = [Column(**field.dict(), **table_kwargs) for field in self.fields]
        return columns

    def get_edges(self) -> List["Edge"]:
        table = api.Table(
            id=self.id, name=self.name, schema=self.table_schema, active=self.active, db_id=self.db_id, db=self.db
        )
        edges = [Edge(namespace=self.namespace, source=column, destination=table) for column in self.get_columns()]
        return edges


class Table(MetabaseModelDefaults, api.Table):
    obj_type: Literal["Table"] = "Table"

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.name}"


class Collection(MetabaseModelDefaults, api.Collection):
    obj_type: Literal["Collection"] = "Collection"

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
