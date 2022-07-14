from pydantic import BaseModel
from typing import Optional, Dict, Union
from uuid import UUID


class BaseNode(BaseModel):
    id: UUID
    name: str
    namespace: str
    data_source: str
    display_name: Optional[str]
    is_active: Optional[str]
    metadata: Optional[Dict] = {}


class EdgeNodeValues(BaseModel):
    name: str
    namespace: str


class BaseEdge(BaseModel):
    id: UUID
    data_source: str
    source: Union[EdgeNodeValues, UUID]
    destination: Union[EdgeNodeValues, UUID]
    is_active: Optional[bool] = True
    metadata: Optional[Dict] = {}
