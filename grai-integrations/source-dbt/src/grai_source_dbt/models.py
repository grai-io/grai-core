from enum import Enum
from itertools import chain
from pathlib import Path
from typing import Annotated, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


class DBTNode(BaseModel):
    pass


class ID(DBTNode):
    name: str


class TableID(ID):
    unique_id: str
    database: str
    table_schema: str = Field(alias="schema")
    namespace: str = Field(alias="package_name")

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.name}"


class ColumnID(ID):
    table_name: str
    table_schema: str
    namespace: str
    database: str

    @property
    def full_name(self):
        return f"{self.table_schema}.{self.table_name}.{self.name}"


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


class NodeConfig(BaseModel):
    materialized: Optional[DbtMaterializationType]


class Column(ColumnID):
    description: Optional[str]
    meta: Dict
    data_type: Optional[str]
    quote: Optional[str]
    tags: List


def make_depends_on_edge(depends_on_node_id: str, model_node):
    return Edge(
        constraint_type=Constraint("dbtm"),
        source=TableID(
            unique_id=depends_on_node_id,
            name=depends_on_node_id.split(".")[1],
            package_name=model_node.package_name,
        ),
        destination=model_node,
        definition=model_node.raw_sql if hasattr(model_node, "raw_sql") else None,
    )


def get_table_from_id_str(unique_id: str):

    id_items = unique_id.split(".")
    model_type, package_name = id_items[0], id_items[1]
    if model_type == "source":
        name, table_name = id_items[2], id_items[3]
        result = SourceResourceType(
            unique_id=unique_id,
            description="",
            config=NodeConfig(materialized=None),
            package_name=package_name,
            name=table_name,
            raw_sql=None,
            database="test",
        )
    else:
        raise NotImplementedError(f"No implementation for model_type {model_type}")

    return result


class Table(TableID):
    path: Optional[Path]
    description: str
    depends_on: Optional[NodeDeps]
    config: NodeConfig
    columns: Optional[Dict[str, Column]]
    raw_sql: Optional[str]

    @root_validator(pre=True)
    def validate_columns(cls, values):
        node_name = values["name"]
        namespace = values["package_name"]
        schema = values["schema"]
        database = values["database"]
        for name, value in values["columns"].items():
            value["table_name"] = node_name
            value["namespace"] = namespace
            value["table_schema"] = schema
            value["database"] = database

        return values

    def get_edges(self):
        column_edges = (
            Edge(
                constraint_type=Constraint("bt"),
                source=self,
                destination=column,
            )
            for column in self.columns.values()
        )
        model_edges = (
            Edge(
                constraint_type=Constraint("dbtm"),
                source=TableID(
                    unique_id=model,
                    name=model.split(".")[
                        2
                    ],  # unique_id's are {resource_type}.{package_name}.{name} for tables
                    package_name=self.namespace,
                    database=self.database,
                    schema=self.table_schema,
                ),
                destination=self,
                definition=self.raw_sql,
            )
            for model in self.depends_on.nodes
        )

        return list(chain(column_edges, model_edges))


class Edge(BaseModel):
    source: Union[TableID, ColumnID]
    destination: Union[TableID, ColumnID]
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None


class ModelResourceType(Table):
    resource_type: Literal["model"] = "model"


class SeedResourceType(Table):
    resource_type: Literal["seed"] = "seed"


class SourceResourceType(Table):
    resource_type: Literal["source"] = "source"


class AnalysisResourceType(BaseModel):
    resource_type: Literal["analysis"] = "analysis"


class TestResourceType(BaseModel):
    resource_type: Literal["test"] = "test"


class OperationResourceType(BaseModel):
    resource_type: Literal["operation"] = "operation"


NodeTypes = Union[
    ModelResourceType,
    SeedResourceType,
    SourceResourceType,
    AnalysisResourceType,
    TestResourceType,
]
SupportedNodeTypes = Union[ModelResourceType, SeedResourceType, SourceResourceType]

Node = Annotated[NodeTypes, Field(discriminator="resource_type")]
