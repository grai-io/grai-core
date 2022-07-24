import json
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Optional

import networkx as nx
from pydantic import BaseModel, validator


class DbtResourceType(str, Enum):
    model = "model"
    analysis = "analysis"
    test = "test"
    operation = "operation"
    seed = "seed"
    source = "source"


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


class Node(BaseModel):
    unique_id: str
    path: Path
    resource_type: DbtResourceType
    description: str
    depends_on: Optional[NodeDeps]
    config: NodeConfig


class Manifest(BaseModel):
    nodes: Dict["str", Node]
    sources: Dict["str", Node]

    @validator("nodes", "sources")
    def filter(cls, val):
        return {
            k: v
            for k, v in val.items()
            if v.resource_type.value in ("model", "seed", "source")
        }

    @classmethod
    def load(cls, manifest_file: str):
        with open(manifest_file) as f:
            data = json.load(f)
        return cls(**data)


class GraphManifest(Manifest):
    @cached_property
    def graph(self):
        return self.build_graph()

    @property
    def node_list(self):
        return list(self.nodes.keys()) + list(self.sources.keys())

    @property
    def edge_list(self):
        return [(k, d) for k, v in self.nodes.items() for d in v.depends_on.nodes]

    def build_graph(self) -> nx.diGraph:
        G = nx.diGraph()
        G.add_nodes_from(self.node_list)
        G.add_edges_from(self.edge_list)
        return G
