import json
from functools import cached_property
from itertools import chain
from typing import Dict, List, Mapping, Tuple, Union

from grai_source_dbt.models import (
    Column,
    Constraint,
    Edge,
    GraiNodeTypes,
    ManifestMetadata,
    Model,
    Seed,
    Source,
    SupportedDBTTypes,
    Table,
)
from pydantic import BaseModel, validator


class Manifest(BaseModel):
    nodes: Dict[str, Union[Model, Seed]]
    sources: Dict[str, Source]
    metadata: ManifestMetadata
    macros: Dict
    docs: Dict
    exposures: Dict
    metrics: Dict
    selectors: Dict
    disabled: Dict
    parent_map: Dict[str, List[str]]
    child_map: Dict[str, List[str]]

    @validator("nodes", pre=True)
    def filter(cls, val) -> Dict[str, Dict]:
        return {k: v for k, v in val.items() if v["resource_type"] in {"model", "seed"}}

    @classmethod
    def load(cls, manifest_file: str) -> "Manifest":
        with open(manifest_file) as f:
            data = json.load(f)
        return cls(**data)


class DBTGraph:
    def __init__(self, manifest: Union[Manifest, str], namespace="default"):
        self.manifest = (
            manifest if isinstance(manifest, Manifest) else Manifest.load(manifest)
        )
        for node in self.node_map.values():
            node.namespace = namespace

    @cached_property
    def node_map(self) -> Dict[Union[str, Tuple], SupportedDBTTypes]:
        message = (
            "Node and source names must be unique. This is a defensive bug that should never happen."
            "Please report this to the maintainers."
        )
        assert not self.manifest.nodes.keys() & self.manifest.sources.keys(), message

        node_map: Dict[Union[str, Tuple], SupportedDBTTypes] = {}
        node_map.update(
            {table.unique_id: table for table in self.manifest.nodes.values()}
        )
        node_map.update(
            {source.unique_id: source for source in self.manifest.sources.values()}
        )
        return node_map

    def dbt_nodes(self) -> List[SupportedDBTTypes]:
        return list(self.node_map.values())

    @cached_property
    def columns(self) -> Dict[Tuple[str, str], Column]:
        columns = {}
        for table in self.manifest.nodes.values():
            for dbt_column in table.columns.values():
                column = Column.from_table_column(table, dbt_column)
                columns[(column.table_unique_id, column.name)] = column
        return columns

    def get_column_edges(self) -> List[Edge]:
        edges = [
            Edge(
                constraint_type=Constraint("bt"),
                source=node,
                destination=self.columns[(node.unique_id, column_str)],
            )
            for node in self.dbt_nodes()
            for column_str in node.columns
        ]
        return edges

    def get_depends_on_edges(self) -> List[Edge]:
        edges = [
            Edge(
                constraint_type=Constraint("dbtm"),
                source=self.node_map[parent_str],
                destination=node,
                definition=self.node_map[parent_str].raw_sql,
            )
            for node in self.dbt_nodes()
            for parent_str in node.depends_on.nodes
        ]
        return edges

    @cached_property
    def nodes(self) -> List[GraiNodeTypes]:
        return list(chain(self.node_map.values(), self.columns.values()))

    @cached_property
    def edges(self) -> List[Edge]:
        return list(chain(self.get_depends_on_edges(), self.get_column_edges()))
