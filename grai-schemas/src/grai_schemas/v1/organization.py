from typing import Literal, Optional
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from pydantic import validator


class OrganisationSpec(GraiBaseModel):
    """Class definition of OrganisationSpec

    Attributes:
        name: The name of the organisation.
        id: Optional UUID of the organisation

    """

    name: str
    id: Optional[UUID]

    def __hash__(self) -> int:
        return hash(self.name)


class OrganisationV1(GraiBaseModel):
    """Class definition of OrganisationV1

    Attributes:
        type: The type of the object e.g. Node, Edge, etc.
        version: The version of the object e.g. v1
        spec: The specification of the object.

    """

    type: Literal["Organisation"]
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
