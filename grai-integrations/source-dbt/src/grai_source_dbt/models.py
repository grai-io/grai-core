from enum import Enum
from itertools import chain
from pathlib import Path
from typing import Annotated, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


class DBTNode(BaseModel):
    pass


class ID(DBTNode):
    name: str
    namespace: str
    full_name: str


class TableID(ID):
    unique_id: str
    table_name: str
    package_name: str

    @root_validator(pre=True)
    def set_defaults(cls, values):
        values.setdefault("full_name", values["unique_id"])
        values.setdefault("namespace", values["package_name"])
        values.setdefault("table_name", values["name"])
        return values


class ColumnID(ID):
    table_name: str

    @root_validator(pre=True)
    def set_defaults(cls, values):
        values.setdefault("full_name", f"{values['table_name']}.{values['name']}")
        return values


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
        definition=model_node.raw_sql if hasattr(model_node, 'raw_sql') else None,
    )


def get_table_from_id_str(unique_id: str):

    id_items = unique_id.split('.')
    model_type, package_name =  id_items[0], id_items[1]
    if model_type == 'source':
        name, table_name = id_items[2], id_items[3]
        result = SourceResourceType(
            unique_id=unique_id,
            description='',
            config=NodeConfig(materialized=None),
            package_name=package_name,
            name=table_name,
            table_name=table_name,
            raw_sql=None,
        )
    else:
        raise NotImplementedError(f"No implementation for model_type {model_type}")

    return result


class Table(TableID):
    unique_id: str
    path: Optional[Path]
    description: str
    depends_on: Optional[NodeDeps]
    config: NodeConfig
    package_name: str
    name: str
    columns: Optional[Dict[str, Column]]
    raw_sql: Optional[str]

    @validator("columns", pre=True)
    def validate_columns(cls, columns, values):
        node_name = values["name"]
        namespace = values["package_name"]
        for name, value in columns.items():
            value["table_name"] = node_name
            value["namespace"] = namespace
        return columns

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
                    name=model.split(".")[1],
                    package_name=self.package_name,
                ),
                destination=self,
                definition=self.raw_sql,
            )
            for model in self.depends_on.nodes
        )
        return list(chain(column_edges, model_edges))


class Edge(BaseModel):
    source: Union[ColumnID, TableID]
    destination: Union[ColumnID, TableID]
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
