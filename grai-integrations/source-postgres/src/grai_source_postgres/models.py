from enum import Enum
from typing import Any, Dict, List, Optional

from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1
from pydantic import BaseModel, Field


class Column(BaseModel):
    name: str = Field(alias="column_name")
    data_type: str
    is_nullable: bool
    default_value: Any = Field(alias="column_default")
    is_pk: Optional[bool]

    class Config:
        allow_population_by_field_name = True


class Table(BaseModel):
    name: str = Field(alias="table_name")
    table_schema: str = Field(alias="schema")
    columns: Optional[List[Column]] = []
    metadata: Optional[Dict] = {}

    class Config:
        allow_population_by_field_name = True


class ColumnID(BaseModel):
    table_schema: str
    table_name: str
    name: str


class Constraint(str, Enum):
    foreign_key = "f"
    primary_key = "p"


class Edge(BaseModel):
    source: ColumnID
    destination: ColumnID
    definition: str
    constraint_type: Constraint


class EdgeQuery(BaseModel):
    constraint_name: str
    constraint_type: str
    self_schema: str
    self_table: str
    self_columns: List[str]
    foreign_schema: str
    foreign_table: str
    foreign_columns: List[str]
    definition: str

    def to_edge(self) -> Edge:
        assert len(self.self_columns) == 1 and len(self.foreign_columns) == 1
        source = ColumnID(
            table_schema=self.self_schema,
            table_name=self.self_table,
            name=self.self_columns[0],
        )
        destination = ColumnID(
            table_schema=self.foreign_schema,
            table_name=self.foreign_table,
            name=self.foreign_columns[0],
        )
        return Edge(
            definition=self.definition,
            source=source,
            destination=destination,
            constraint_type=self.constraint_type,
        )


class Node(BaseModel):
    name: str
    namespace: str = "default"
    data_source: str = "postgres"
    metadata: Dict = {}


def build_node(
    table: Table,
    column: Column,
    namespace: str = "default",
    data_source: str = "postgres",
) -> Node:
    return Node(
        name=column.name,
        namespace=namespace,
        data_source=data_source,
    )
