from typing import Literal, Optional
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from pydantic import validator


class OrganisationSpec(GraiBaseModel):
    name: str
    id: Optional[UUID]

    def __hash__(self) -> int:
        return hash(self.name)


class OrganisationV1(GraiBaseModel):
    type: Literal["Organisation", "Organization"]
    version: Literal["v1"] = "v1"
    spec: OrganisationSpec

    @validator("type")
    def validate_org_type(cls, v):
        if v == "Organization":
            return "Organisation"
        return v

    def __hash__(self) -> int:
        return hash(self.spec)

    @classmethod
    def from_spec(cls, spec_dict: dict) -> "OrganisationV1":
        """

        Args:
            spec_dict (Dict):

        Returns:

        Raises:

        """
        return cls(version="v1", type="Organisation", spec=spec_dict)


__all__ = ["OrganisationSpec", "OrganisationV1"]
