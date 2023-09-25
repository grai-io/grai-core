from typing import List, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.workspace import WorkspaceSpec
from pydantic import validator


class SourceSpec(GraiBaseModel):
    """Class definition of SourceSpec

    Attributes:
        id: An optional UUID of the source.
        name: The name of the source.
        workspace: The workspace the source belongs to.

    """

    id: Optional[UUID]
    name: str
    workspace: Union[UUID, WorkspaceSpec, None]

    @property
    def workspace_id(self) -> Optional[UUID]:
        return self.workspace.id if isinstance(self.workspace, WorkspaceSpec) else self.workspace

    def __hash__(self) -> int:
        return hash(self.name)


class DataSourceMixin(GraiBaseModel):
    """Class definition of DataSourceMixin

    Attributes:
        data_source: The data source which created this object.

    """

    data_source: SourceSpec


class DataSourcesMixin(GraiBaseModel):
    """Class definition of DataSourcesMixin

    Attributes:
        data_sources: The data sources which created this object.

    """

    data_sources: List[Union[UUID, SourceSpec]]


class SourceV1(GraiBaseModel):
    """Class definition of SourceV1

    Attributes:
        type: A string indicating the type of the object. In this case it is "Source".
        version: The version of the object e.g. "v1".
        spec: The specification of the object.

    """

    type: Literal["Source"] = "Source"
    version: Literal["v1"] = "v1"
    spec: SourceSpec

    def __hash__(self):
        return hash(self.spec)

    @classmethod
    def from_spec(cls, spec: Union[dict, SourceSpec]) -> "SourceV1":
        """

        Args:
            spec: The specification of the object.

        Returns:

        Raises:

        """
        return cls(version="v1", type="Source", spec=spec)


__all__ = ["SourceSpec", "SourceV1", "DataSourceMixin", "DataSourcesMixin"]
