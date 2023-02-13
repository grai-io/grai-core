from __future__ import annotations

from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from grai_source_dbt.models.shared import (
    ID,
    Constraint,
    DBTNode,
    DBTNodeColumn,
    NodeDeps,
)
from grai_source_dbt.models.tests import Test


class Table(DBTNode):
    table_schema: str = Field(alias="schema")

    #### Grai Specific ####
    tests: Optional[List[Test]] = []

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.name}"


class Model(Table):
    resource_type: Literal["model"]


class Source(Table):
    resource_type: Literal["source"]
    identifier: str
    depends_on: NodeDeps = NodeDeps(nodes=[], macros=[])

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.identifier}"


class Seed(DBTNode):
    table_schema: str = Field(alias="schema")
    path: str
    original_file_path: str
    resource_type: Literal["seed"]

    #### Grai Specific ####
    tests: Optional[List[Test]] = []


class Snapshot(DBTNode):
    resource_type: Literal["snapshot"]
    depends_on: NodeDeps = NodeDeps(nodes=[], macros=[])


class Column(ID):
    name: str
    description: Optional[str]
    meta: Dict
    data_type: Optional[str]
    quote: Optional[str]
    tags: List
    table_unique_id: str
    table_name: str
    table_schema: str
    database: str
    resource_type: Literal["column"] = "column"

    #### Grai Specific ####
    tests: Optional[List[Test]] = []

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.table_name}.{self.name}"

    @classmethod
    def from_table_column(cls, table: DBTNode, column: DBTNodeColumn) -> "Column":
        attrs = {
            "table_unique_id": table.unique_id,
            "table_name": table.name,
            "table_schema": table.node_schema,
            "database": table.database,
            "namespace": table.namespace,
            "package_name": table.package_name,
        }
        attrs.update(column.dict())
        return cls(**attrs)

    @property
    def unique_id(self):
        return self.table_unique_id, self.name

    def __hash__(self):
        return hash((self.table_unique_id, self.name))


SupportedDBTTypes = Union[Model, Source, Seed, Snapshot]
GraiNodeTypes = Union[Model, Source, Seed, Column]


class Edge(BaseModel):
    source: GraiNodeTypes
    destination: GraiNodeTypes
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None

    def __hash__(self):
        return hash((self.source, self.destination))
