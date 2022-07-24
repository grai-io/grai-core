from typing import Dict, Optional, Union
from uuid import UUID

from pydantic import BaseModel


class BaseNode(BaseModel):
    id: Union[UUID, str]
    name: str
    namespace: str
    data_source: str
    display_name: Optional[str]
    is_active: Optional[bool]
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
