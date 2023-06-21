from typing import List, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.workspace import WorkspaceSpec
from pydantic import validator


class SourceSpec(GraiBaseModel):
    id: Optional[UUID]
    name: str
    workspace: Union[UUID, WorkspaceSpec]

    @property
    def workspace_id(self) -> Optional[UUID]:
        return self.workspace if isinstance(self.workspace, UUID) else self.workspace.id

    @validator("workspace", pre=True)
    def validate_workspace(cls, v):
        if isinstance(v, str):
            return v
        return WorkspaceSpec(**v)

    def __hash__(self) -> int:
        if self.workspace_id is None:
            raise ValueError("Cannot hash a source spec without a workspace id")
        return hash((self.name, self.workspace_id))


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

    @classmethod
    def from_spec(cls, spec_dict: dict) -> "SourceV1":
        """

        Args:
            spec_dict (Dict):

        Returns:

        Raises:

        """
        return cls(version="v1", type="Source", spec=spec_dict)


__all__ = ["SourceSpec", "SourceV1", "DataSourceMixin", "DataSourcesMixin"]
