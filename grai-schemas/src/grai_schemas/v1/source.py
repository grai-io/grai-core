from datetime import datetime
from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.workspace import WorkspaceSpec
from pydantic import JSON


class SourceSpec(GraiBaseModel):
    id: Optional[UUID]
    name: str
    workspace: Union[str, WorkspaceSpec]

    @property
    def workspace_name(self) -> str:
        return self.workspace if isinstance(self.workspace, str) else self.workspace.name

    def __hash__(self) -> int:
        return hash((self.name, self.workspace_name))


class Source(GraiBaseModel):
    type: Literal["Source"] = "Source"
    version: Literal["v1"] = "v1"
    spec: SourceSpec

    def __hash__(self):
        return hash(self.spec)


class EventSpec(GraiBaseModel):
    id: UUID
    connection_id: UUID
    date: datetime
    workspace: Union[str, WorkspaceSpec]
    diff: JSON

    def __hash__(self) -> int:
        return hash(self.id)


class Event(GraiBaseModel):
    type: Literal["Event"] = "Event"
    version: Literal["v1"] = "v1"
    spec: EventSpec

    def __hash__(self):
        return hash(self.spec)
