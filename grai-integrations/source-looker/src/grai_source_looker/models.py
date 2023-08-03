from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


class LookerNode(BaseModel):
    """ """

    pass


class ID(LookerNode):
    """ """

    name: str
    namespace: str
    full_name: str

    class Config:
        """ """

        extra = "forbid"


class TableID(ID):
    """ """

    # table_schema: str

    @root_validator(pre=True)
    def make_full_name(cls, values):
        """

        Args:
            values:

        Returns:

        Raises:

        """
        if values.get("full_name", None) is None:
            # values["full_name"] = f"{values['table_schema']}.{values['name']}"
            values["full_name"] = values["name"]
        return values


class FieldID(ID):
    """ """

    # table_schema: str
    table_name: str

    @root_validator(pre=True)
    def make_full_name(cls, values):
        """

        Args:
            values:

        Returns:

        Raises:

        """
        if values.get("full_name", None) is None:
            # values[
            #     "full_name"
            # ] = f"{values['table_schema']}.{values['table_name']}.{values['name']}"
            values["full_name"] = values["name"]
        return values


class QueryField(LookerNode):
    name: str


class Query(LookerNode):
    fields: List[str]


class DashboardElement(LookerNode):
    query: Optional[Query]


class Constraint(str, Enum):
    """ """

    foreign_key = "f"
    primary_key = "p"
    belongs_to = "bt"


class Edge(BaseModel):
    """ """

    source: Union[FieldID, TableID]
    destination: Union[FieldID, TableID]
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None


class Dashboard(LookerNode):
    """ """

    name: str = Field(alias="id")
    display_name: str = Field(alias="title")
    dashboard_elements: Optional[List[DashboardElement]] = Field(alias="dashboard_elements")

    def get_fields(self):
        """ """

        fields = []

        for element in self.dashboard_elements if self.dashboard_elements else []:
            if element.query:
                fields.extend([QueryField(name=field) for field in element.query.fields])

        return fields

    def get_edges(self):
        """ """

        edges = []

        for element in self.dashboard_elements if self.dashboard_elements else []:
            if element.query:
                edges.extend(
                    [
                        Edge(
                            constraint_type=Constraint("bt"),
                            source=TableID(
                                name=self.name,
                                namespace="looker",
                            ),
                            destination=FieldID(
                                table_name=self.name,
                                name=field,
                                namespace="looker",
                            ),
                        )
                        for field in element.query.fields
                    ]
                )

        return edges
