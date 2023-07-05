from typing import List, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.workspace import WorkspaceSpec
from pydantic import validator


class SourceSpec(GraiBaseModel):
    id: Optional[UUID]
    name: str
    workspace: Union[UUID, WorkspaceSpec, None]

    @property
    def workspace_id(self) -> Optional[UUID]:
        return self.workspace.id if isinstance(self.workspace, WorkspaceSpec) else self.workspace

    def __hash__(self) -> int:
        return hash(self.name)


class DataSourceMixin(GraiBaseModel):
    data_source: SourceSpec


class DataSourcesMixin(GraiBaseModel):
    data_sources: List[Union[UUID, SourceSpec]]


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
