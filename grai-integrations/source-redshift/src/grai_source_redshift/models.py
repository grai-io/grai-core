from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


class RedshiftNode(BaseModel):
    """ """

    pass


class ID(RedshiftNode):
    """ """

    name: str
    namespace: str
    full_name: str

    class Config:
        """ """

        extra = "forbid"


class TableID(ID):
    """ """

    table_schema: str
    name: str

    @root_validator(pre=True)
    def make_full_name(cls, values):
        """

        Args:
            values:

        Returns:

        Raises:

        """
        full_name = values.get("full_name", None)
        if values.get("full_name", None) is None:
            values["full_name"] = f"{values['table_schema']}.{values['name']}"
        return values


class ColumnID(ID):
    """ """

    table_schema: str
    table_name: str
    name: str

    @root_validator(pre=True)
    def make_full_name(cls, values):
        """

        Args:
            values:

        Returns:

        Raises:

        """
        full_name = values.get("full_name", None)
        if values.get("full_name", None) is None:
            values["full_name"] = f"{values['table_schema']}.{values['table_name']}.{values['name']}"
        return values


class ColumnConstraint(Enum):
    """ """

    primary_key = "p"
    unique = "u"
    foreign_key = "f"
    check = "c"
    trigger = "t"
    exclusion = "x"


UNIQUE_COLUMN_CONSTRAINTS = {ColumnConstraint.primary_key.value, ColumnConstraint.unique.value}


class Column(RedshiftNode):
    """ """

    name: str = Field(alias="column_name")
    table: str = Field(alias="table_name")
    column_schema: str = Field(alias="schema")
    data_type: str
    is_nullable: bool
    namespace: str
    default_value: Any = Field(alias="column_default")
    column_constraint: Optional[ColumnConstraint]
    is_pk: Optional[bool] = False
    full_name: Optional[str] = None

    class Config:
        """ """

        allow_population_by_field_name = True

    @validator("full_name", always=True)
    def make_full_name(cls, full_name, values):
        """

        Args:
            full_name:
            values:

        Returns:

        Raises:

        """
        if full_name is not None:
            return full_name
        result = f"{values['column_schema']}.{values['table']}.{values['name']}"
        return result


class LateBindingViewColumn(RedshiftNode):
    name: str = Field(alias="column_name")
    table: str = Field(alias="table_name")
    column_schema: str = Field(alias="schema")
    namespace: str
    data_type: str

    class Config:
        """ """

        allow_population_by_field_name = True

    @property
    def full_name(self):
        return f"{self.column_schema}.{self.table}.{self.name}"


class Constraint(str, Enum):
    """ """

    foreign_key = "FOREIGN KEY"
    primary_key = "PRIMARY KEY"
    belongs_to = "bt"


class Edge(BaseModel):
    """ """

    source: Union[ColumnID, TableID]
    destination: Union[ColumnID, TableID]
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None


class TableType(str, Enum):
    """ """

    Table = "BASE TABLE"
    View = "VIEW"
    ForeignTable = "FOREIGN"
    TemporaryTable = "LOCAL TEMPORARY"


class Table(RedshiftNode):
    """ """

    name: str = Field(alias="table_name")
    table_schema: str = Field(alias="schema")
    table_type: TableType
    namespace: str
    columns: Optional[List[Column]] = []
    metadata: Dict = {}
    full_name: Optional[str] = None

    class Config:
        """ """

        allow_population_by_field_name = True

    @validator("full_name", always=True)
    def make_full_name(cls, full_name, values):
        """

        Args:
            full_name:
            values:

        Returns:

        Raises:

        """
        if full_name is not None:
            return full_name

        return f"{values['table_schema']}.{values['name']}"

    def get_edges(self):
        """ """
        return [
            Edge(
                constraint_type=Constraint("bt"),
                source=TableID(
                    table_schema=self.table_schema,
                    name=self.name,
                    namespace=self.namespace,
                ),
                destination=ColumnID(
                    table_schema=self.table_schema,
                    table_name=self.name,
                    name=column.name,
                    namespace=self.namespace,
                ),
            )
            for column in self.columns
        ]


class EdgeQuery(BaseModel):
    """ """

    namespace: str
    constraint_name: str
    constraint_type: str
    self_schema: str
    self_table: str
    self_column: str
    foreign_schema: str
    foreign_table: str
    foreign_column: str

    def to_edge(self) -> Edge:
        """

        Args:

        Returns:

        Raises:

        """
        destination = ColumnID(
            table_schema=self.self_schema,
            table_name=self.self_table,
            name=self.self_column,
            namespace=self.namespace,
        )
        source = ColumnID(
            table_schema=self.foreign_schema,
            table_name=self.foreign_table,
            name=self.foreign_column,
            namespace=self.namespace,
        )
        return Edge(
            source=source,
            destination=destination,
            constraint_type=self.constraint_type,
        )
