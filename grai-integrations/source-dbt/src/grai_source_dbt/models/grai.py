from __future__ import annotations

import typing
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from grai_schemas.v1.metadata.edges import EdgeMetadataTypeLabels
from pydantic import BaseModel, Field

from grai_source_dbt.models.shared import (
    ID,
    Constraint,
    DBTNode,
    DBTNodeColumn,
    NodeDeps,
)

if typing.TYPE_CHECKING:
    from grai_source_dbt.loaders import NodeTypes


class Column(ID):
    """ """

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
    tests: List = []

    @property
    def full_name(self):
        """ """
        return f"{self.table_schema}.{self.table_name}.{self.name}"

    @classmethod
    def from_table_column(cls, table: NodeTypes, column, namespace) -> "Column":
        """

        Args:
            table (NodeTypes):
            column:
            namespace:

        Returns:

        Raises:

        """
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
        """ """
        return self.table_unique_id, self.name

    def __hash__(self):
        return hash((self.table_unique_id, self.name))

    class Config:
        """ """

        validate_assignment = True


class EdgeTerminus(BaseModel):
    """ """

    name: str
    namespace: str

    @property
    def identifier(self):
        """ """
        return f"{self.namespace}:{self.name}"

    class Config:
        """ """

        validate_assignment = True


class Edge(BaseModel):
    """ """

    source: EdgeTerminus
    destination: EdgeTerminus
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None
    edge_type: EdgeMetadataTypeLabels

    def __hash__(self):
        return hash((self.source, self.destination))

    @property
    def name(self):
        """ """
        return f"{self.source.identifier} -> {self.destination.identifier}"

    class Config:
        """ """

        validate_assignment = True
