import json
import re
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
            # values["full_name"] = f"{values['table_name']}.{values['name']}"
            values["full_name"] = values["name"]
        return values


class Dimension(LookerNode):
    name: str
    namespace: Optional[str]
    label: str
    type: str
    sql: str
    table_name: Optional[str]

    @property
    def column_name(self):
        return re.sub("\${TABLE}", self.table_name, self.sql.strip())


class ExploreFields(LookerNode):
    dimensions: List[Dimension]


class Explore(LookerNode):
    id: str
    name: str
    namespace: Optional[str]
    fields: ExploreFields
    sql_table_name: str

    @property
    def table_name(self):
        res = re.search("`([\w_\.]*)`", self.sql_table_name)

        if res:
            return res.group(1)

        return self.sql_table_name


class QueryField(LookerNode):
    namespace: str
    name: str


class DynamicField(LookerNode):
    measure: str
    based_on: str


class Query(LookerNode):
    id: int
    title: Optional[str]
    namespace: Optional[str]
    model: str
    view: str
    fields: List[str]
    dynamic_fields: Optional[str]
    dashboard_name: Optional[str]

    @property
    def dynamic_fields_map(self):
        if not self.dynamic_fields:
            return {}

        result = {}

        try:
            for f in json.loads(self.dynamic_fields):
                category = f.get("category")

                if category == "measure":
                    result[f["measure"]] = f["based_on"]
                elif category == "dimension":
                    # result[f["dimension"]] = f["expression"]
                    pass
                elif category == "table_calculation":
                    pass
                elif not category and f.get("measure") and f.get("based_on"):
                    result[f["measure"]] = f["based_on"]
                else:
                    print("Unknown category: ", f["category"])
                    print(self.dynamic_fields)

            return result
        except:
            print(self.dynamic_fields)
            raise


class ResultMaker(LookerNode):
    id: int
    query: Optional[Query]
    dynamic_fields: Optional[str]


class DashboardElement(LookerNode):
    id: int
    title: Optional[str]
    result_maker: Optional[ResultMaker]


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

    namespace: str
    name: str = Field(alias="id")
    display_name: str = Field(alias="title")
    dashboard_elements: Optional[List[DashboardElement]]

    def get_query(self, element):
        if element.result_maker and element.result_maker.query:
            return element.result_maker.query

    def get_queries(self):
        """ """

        queries = []

        for element in self.dashboard_elements if self.dashboard_elements else []:
            query = self.get_query(element)

            if query:
                query.title = element.title
                query.namespace = self.namespace
                query.dynamic_fields = element.result_maker.dynamic_fields
                query.dashboard_name = self.name

                queries.append(query)

        return queries

    def get_query_edges(self):
        """ """

        edges = []

        for element in self.dashboard_elements if self.dashboard_elements else []:
            query = self.get_query(element)

            if query:
                edges.append(
                    Edge(
                        constraint_type=Constraint("bt"),
                        source=TableID(
                            name=self.name,
                            namespace=self.namespace,
                        ),
                        destination=FieldID(
                            table_name=self.name,
                            name=element.title if element.title else element.id,
                            namespace=self.namespace,
                        ),
                    )
                )

        return edges
