from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel


class OrganizationSpec(GraiBaseModel):
    name: str
    id: Optional[UUID]

    def __hash__(self) -> int:
        return hash(self.name)


class OrganizationV1(GraiBaseModel):
    type: Literal["Organization"] = "Organization"
    version: Literal["v1"] = "v1"
    spec: OrganizationSpec


class WorkspaceSpec(GraiBaseModel):
    name: str
    id: Optional[UUID]
    organization: Union[str, OrganizationSpec]
    search_enabled: Optional[bool]

    @property
    def organization_name(self) -> str:
        return self.organization if isinstance(self.organization, str) else self.organization.name

    @property
    def workspace_ref(self) -> str:
        return f"{self.organization_name}/{self.name}"

    def __hash__(self) -> int:
        return hash(self.name)


class WorkspaceV1(GraiBaseModel):
    type: Literal["Workspace"] = "Workspace"
    version: Literal["v1"] = "v1"
    spec: WorkspaceSpec

    def __hash__(self) -> int:
        return hash(self.spec)
