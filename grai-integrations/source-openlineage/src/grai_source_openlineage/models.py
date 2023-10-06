from enum import Enum
from typing import Dict, Optional, Union

from pydantic import BaseModel


class Table(BaseModel):
    """ """

    namespace: str
    name: str

    def __hash__(self):
        return hash((self.name, self.namespace))


class Column(BaseModel):
    """ """

    namespace: str
    name: str
    table_name: str

    def __hash__(self):
        return hash((self.name, self.namespace))


NodeTypes = Union[Column, Table]


class Constraint(str, Enum):
    """ """

    foreign_key = "f"
    belongs_to = "bt"
    copy = "c"


class Edge(BaseModel):
    source: NodeTypes
    destination: NodeTypes

    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None
