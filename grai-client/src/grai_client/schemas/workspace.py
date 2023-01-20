from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class Workspace(BaseModel):
    name: str
    id: UUID


WorkspaceLabels = Literal["workspace", "workspaces", "Workspace", "Workspaces"]
