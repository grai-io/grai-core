from uuid import UUID

from pydantic import BaseModel


class Workspace(BaseModel):
    """ """

    name: str
    ref: str
    id: UUID
