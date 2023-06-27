from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union
from enum import Enum


class Question(BaseModel):
    """ """

    id: int
    name: str
    description: str
    result_metadata: List[Dict[str, Any]]
    creator: Dict[str, Any]
    database_id: int
    table_id: int
    collection: Dict[str, Any]
    public_uuid: str
    namespace: str


class Table(BaseModel):
    """ """

    id: int
    db_id: int
    name: str
    display_name: str
    schema: str
    description: str
    db: Dict[str, Any]
    entity_type: str
    namespace: str

    @property
    def full_name(self):
        return f"{self.schema}.{self.name}"


class Constraint(str, Enum):
    """ """

    belongs_to = "bt"
    copy = "c"


NodeTypes = Union[Question, Table]


class Edge(BaseModel):
    """ """

    source: NodeTypes
    destination: NodeTypes
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None

    def __hash__(self):
        return hash((self.source, self.destination))
