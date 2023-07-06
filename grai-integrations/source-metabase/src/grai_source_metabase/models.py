from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Question(BaseModel):
    id: int
    name: str
    creator: Dict[str, Any]
    database_id: int
    namespace: str

    @property
    def full_name(self):
        return f"{self.name}.{self.id}"


class Table(BaseModel):
    id: int
    db_id: int
    name: str
    display_name: str
    schema_name: str
    db: Dict[str, Any]
    namespace: str

    @property
    def full_name(self):
        return f"{self.schema_name}.{self.name}"


NodeTypes = Union[Question, Table]


class Edge(BaseModel):
    source: NodeTypes
    destination: NodeTypes
    definition: Optional[str]
    metadata: Optional[Dict] = None

    def __hash__(self):
        return hash((self.source, self.destination))
