from datetime import datetime
from typing import Dict, List, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.workspace import WorkspaceSpec
from pydantic import BaseModel, Json


class SourceSpec(GraiBaseModel):
    id: Optional[UUID]
    name: str
    workspace: Union[str, WorkspaceSpec]

    @property
    def workspace_name(self) -> str:
        return self.workspace if isinstance(self.workspace, str) else self.workspace.name

    def __hash__(self) -> int:
        return hash((self.name, self.workspace_name))


class DataSourceMixin(GraiBaseModel):
    data_source: SourceSpec


class DataSourcesMixin(GraiBaseModel):
    data_sources: Optional[List[Union[str, SourceSpec]]]


class SourceV1(GraiBaseModel):
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
    diff: Json

    def __hash__(self) -> int:
        return hash(self.id)


class EventV1(GraiBaseModel):
    type: Literal["Event"] = "Event"
    version: Literal["v1"] = "v1"
    spec: EventSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "EventV1":
        """

        Args:
            spec_dict (Dict):

        Returns:

        Raises:

        """
        return cls(version="v1", type="Event", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)
