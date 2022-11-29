import json
from functools import cached_property
from itertools import chain
from typing import Dict, List, Union

from grai_source_dbt.models import (
    Column,
    Edge,
    SupportedNodeTypes,
    Table,
    get_table_from_id_str,
)
from pydantic import BaseModel, validator


class Manifest(BaseModel):
    nodes: Dict[str, SupportedNodeTypes]

    @validator("nodes", pre=True)
    def filter(cls, val):
        return {
            k: v
            for k, v in val.items()
            if v["resource_type"] in {"model", "source", "seed"}
        }

    @classmethod
    def load(cls, manifest_file: str):
        with open(manifest_file) as f:
            data = json.load(f)
        return cls(**data)


class DBTGraph:
    def __init__(self, manifest: Manifest):
        self.manifest = manifest

    @cached_property
    def nodes(self) -> List[Union[Table, Column]]:
        nodes = list(self.manifest.nodes.values())
        column_nodes = chain(
            *(vals for node in nodes if (vals := node.columns.values()))
        )

        # Sources don't appear to be included in the list of nodes
        source_nodes = [
            get_table_from_id_str(edge.source.full_name)
            for edge in self.edges
            if edge.source.full_name.startswith("source")
        ]

        nodes = list(chain(nodes, column_nodes, source_nodes))
        return nodes

    @cached_property
    def edges(self) -> List[Edge]:
        return [
            edge for node in self.manifest.nodes.values() for edge in node.get_edges()
        ]
