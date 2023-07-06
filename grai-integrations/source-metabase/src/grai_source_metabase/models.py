from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Question(BaseModel):
    id: int
    name: str
    creator: Dict[str, Any]
    database_id: int
    table_id: int | None
    collection: Dict[str, Any] | None
    public_uuid: str | None
    namespace: str


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
