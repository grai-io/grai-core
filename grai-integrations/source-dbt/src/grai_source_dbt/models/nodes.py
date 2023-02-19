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
from grai_source_dbt.versions import NodeTypes


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
    def from_table_column(cls, table: NodeTypes, column, namespace) -> "Column":
        attrs = {
            "table_unique_id": table.unique_id,
            "table_name": table.name,
            "table_schema": table.schema_,
            "database": table.database,
            "namespace": namespace,
            "package_name": table.package_name,
        }
        attrs.update(column.dict())
        return cls(**attrs)

    @property
    def unique_id(self):
        return self.table_unique_id, self.name

    def __hash__(self):
        return hash((self.table_unique_id, self.name))


class EdgeTerminus(BaseModel):
    name: str
    namespace: str

    @property
    def identifier(self):
        return f"{self.namespace}:{self.name}"


class Edge(BaseModel):
    source: EdgeTerminus
    destination: EdgeTerminus
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None

    def __hash__(self):
        return hash((self.source, self.destination))

    @property
    def name(self):
        return f"{self.source.identifier} -> {self.destination.identifier}"
