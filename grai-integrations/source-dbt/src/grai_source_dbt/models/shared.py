from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class ManifestMetadata(BaseModel):
    """ """

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
    """ """

    name: str
    namespace: Optional[str]
    package_name: str


class Constraint(str, Enum):
    """ """

    belongs_to = "bt"
    dbt_model = "dbtm"


class DbtResourceType(str, Enum):
    """ """

    model = "model"
    seed = "seed"
    source = "source"
    analysis = "analysis"
    test = "test"
    operation = "operation"


class DbtMaterializationType(str, Enum):
    """ """

    table = "table"
    view = "view"
    incremental = "incremental"
    ephemeral = "ephemeral"
    seed = "seed"
    snapshot = "snapshot"


class NodeDeps(BaseModel):
    """ """

    nodes: List[str]
    macros: List[str]  # TODO: macros not currently tested


class NodeConfig(BaseModel):
    """ """

    materialized: Optional[DbtMaterializationType]


class DBTNodeColumn(BaseModel):
    """ """

    name: str
    description: Optional[str]
    meta: Dict
    data_type: Optional[str]
    quote: Optional[str]
    tags: List


class NodeChecksum(BaseModel):
    """ """

    name: str
    checksum: str


class NodeDocs(BaseModel):
    """ """

    show: bool


class DBTNode(ID):
    """ """

    unique_id: str
    root_path: str
    path: Optional[str]
    original_file_path: Optional[str]
    node_schema: str = Field(alias="schema")
    description: str
    depends_on: NodeDeps
    config: NodeConfig
    columns: Dict[str, DBTNodeColumn]
    raw_sql: Optional[str]
    database: str
    fqn: List[str]
    alias: Optional[str]
    checksum: Optional[NodeChecksum]
    tags: Union[str, List[str]]
    refs: Optional[List[List[str]]]
    sources: Optional[List[List[str]]]
    meta: Dict
    docs: Optional[NodeDocs]
    patch_path: Any
    compiled_path: Any
    deferred: Optional[bool]
    unrendered_config: Dict[Any, Any]
    created_at: float

    @property
    def tag_list(self) -> List[str]:
        """

        Args:

        Returns:

        Raises:

        """
        return [self.tags] if isinstance(self.tags, str) else self.tags

    def __hash__(self):
        return hash(self.unique_id)

    @property
    def full_name(self):
        """ """
        return f"{self.node_schema}.{self.name}"
