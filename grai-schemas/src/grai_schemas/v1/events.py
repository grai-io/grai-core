from datetime import datetime
from typing import Dict, Literal, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.workspace import WorkspaceSpec
from pydantic import Json


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
