from datetime import datetime
from typing import Dict, Literal, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.workspace import WorkspaceSpec
from pydantic import Json


class EventSpec(GraiBaseModel):
    """Class definition of EventSpec

    Attributes:
        id: UUID of the event.
        connection_id: UUID of the events connection.
        date: Datetime of the event.
        workspace: WorkspaceSpec of the event.
        diff: Json of the changes from the event.

    """

    id: UUID
    connection_id: UUID
    date: datetime
    workspace: Union[str, WorkspaceSpec]
    diff: Json

    def __hash__(self) -> int:
        return hash(self.id)


class EventV1(GraiBaseModel):
    """Class definition of EventV1

    Attributes:
        type: Object type of the Metadata e.g. NodeV1, EdgeV1, etc.
        version: Schema version of the object.
        spec: The event specification.

    """

    type: Literal["Event"] = "Event"
    version: Literal["v1"] = "v1"
    spec: EventSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "EventV1":
        """

        Args:
            spec_dict (Dict):

        Returns:
            An EventV1 instance
        Raises:

        """
        return cls(version="v1", type="Event", spec=spec_dict)

    def __hash__(self):
        return hash(self.spec)
