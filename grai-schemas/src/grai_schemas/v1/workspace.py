import re
from typing import Dict, Literal, Optional, Union
from uuid import UUID

from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.organization import OrganisationSpec
from pydantic import Field, validator


class _DefaultRefSentinel(str):
    pass


_REF_REGEX = re.compile("^[^/]*/[^/]*$")


class WorkspaceSpec(GraiBaseModel):
    id: Optional[UUID]
    name: str
    organisation: Union[UUID, OrganisationSpec] = Field(..., alias="organization")
    ref: str = _DefaultRefSentinel()  # This keeps mypy happy
    search_enabled: Optional[bool]

    @property
    def organization(self):
        return self.organisation

    @validator("organisation", always=True, pre=True)
    def validate_organisation(cls, v: Union[UUID, str, Dict, OrganisationSpec]) -> Union[UUID, OrganisationSpec]:
        if isinstance(v, (OrganisationSpec, UUID)):
            return v
        elif isinstance(v, dict):
            return OrganisationSpec(**v)
        elif isinstance(v, str):
            try:
                uuid_val = UUID(v)
                return uuid_val
            except ValueError:
                return OrganisationSpec(name=v)
        else:
            message = (
                f"Invalid value for organisation: Receive {v} which is of type {type(v)}. You might have meant "
                f"to provide a UUID for the organisation, or a string containing the name of the organisation?"
            )
            raise ValueError(message)

    @validator("ref", always=True, pre=True)
    def validate_ref(cls, v: Optional[str], values, field) -> str:
        if v is None or isinstance(v, _DefaultRefSentinel):
            if isinstance(values.get("organisation", None), OrganisationSpec):
                return f"{values['organisation'].name}/{values['name']}"
            else:
                message = (
                    f"`ref` is a required field when `organisation` is a UUID. Either provide a value for `ref`, or "
                    f" provide an OrganizationSpec to organisation and ref will be automatically generated."
                )
                raise ValueError(message)
        elif re.match(_REF_REGEX, v):
            # TODO: This doesn't cover the case of a user providing a UUID for the organisation
            if isinstance(values.get("organisation", None), OrganisationSpec):
                validated_ref = f"{values['organisation'].name}/{values['name']}"
                message = (
                    f"Attempted to create a workspace with a `ref` of {v}, but this didn't match the specified "
                    f"organisation name ({values['organisation'].name}) and workspace name ({values['name']}). "
                )
                if validated_ref != v:
                    raise ValueError(message)
            return v
        else:
            message = (
                f"Invalid value for `ref`: Received {v}. Expected a string containing a"
                f"single forwards slash (/) separating the organisation name and the workspace name."
                f"e.g. `my-organisation/my-workspace`"
            )
            raise ValueError(message)

    def __hash__(self) -> int:
        return hash(self.ref)


class WorkspaceV1(GraiBaseModel):
    type: Literal["Workspace"] = "Workspace"
    version: Literal["v1"] = "v1"
    spec: WorkspaceSpec

    @classmethod
    def from_spec(cls, spec_dict: Dict) -> "WorkspaceV1":
        """

        Args:
            spec_dict (Dict):

        Returns:

        Raises:

        """
        return cls(version="v1", type="Workspace", spec=spec_dict)

    def __hash__(self) -> int:
        return hash(self.spec)


__all__ = ["WorkspaceSpec", "WorkspaceV1"]
