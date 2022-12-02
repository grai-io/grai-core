from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, root_validator


class ManifestMetadata(BaseModel):
    dbt_schema_version: str
    dbt_version: str
    generated_at: str
    invocation_id: str
    env: Dict
    project_id: UUID
    user_id: UUID
    send_anonymous_usage_stats: bool
    adapter_type: str


class ID(BaseModel):
    name: str
    namespace: Optional[str]
    package_name: str


class Constraint(str, Enum):
    belongs_to = "bt"
    dbt_model = "dbtm"


class DbtResourceType(str, Enum):
    model = "model"
    seed = "seed"
    source = "source"
    analysis = "analysis"
    test = "test"
    operation = "operation"


class DbtMaterializationType(str, Enum):
    table = "table"
    view = "view"
    incremental = "incremental"
    ephemeral = "ephemeral"
    seed = "seed"


class NodeDeps(BaseModel):
    nodes: List[str]
    macros: List[str]  # TODO: macros not currently tested


class NodeConfig(BaseModel):
    materialized: Optional[DbtMaterializationType]


class DBTNodeColumn(BaseModel):
    name: str
    description: Optional[str]
    meta: Dict
    data_type: Optional[str]
    quote: Optional[str]
    tags: List


class DBTNode(ID):
    unique_id: str
    path: Optional[Path]
    original_file_path: Optional[Path]
    description: str
    depends_on: NodeDeps
    config: NodeConfig
    columns: Dict[str, DBTNodeColumn]
    raw_sql: Optional[str]
    database: str
    node_schema: str = Field(alias="schema")

    def __hash__(self):
        return hash(self.unique_id)

    @property
    def full_name(self):
        return f"{self.node_schema}.{self.name}"

    # @property
    # def full_name(self):
    # return f"{self.unique_id}"


class Table(DBTNode):
    table_schema: str = Field(alias="schema")

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.name}"


class Model(Table):
    resource_type: Literal["model"]


class Source(Table):
    resource_type: Literal["source"]
    depends_on: NodeDeps = NodeDeps(nodes=[], macros=[])


class Seed(DBTNode):
    table_schema: str = Field(alias="schema")
    path: Path
    original_file_path: Path
    resource_type: Literal["seed"]


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

    def __hash__(self):
        return hash((self.table_unique_id, self.name))


SupportedDBTTypes = Union[Model, Source, Seed]
GraiNodeTypes = Union[Model, Source, Seed, Column]


class Edge(BaseModel):
    source: GraiNodeTypes
    destination: GraiNodeTypes
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None

    def __hash__(self):
        return hash((self.source, self.destination))
