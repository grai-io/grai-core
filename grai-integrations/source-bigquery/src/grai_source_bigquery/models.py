from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


class BigqueryNode(BaseModel):
    """ """

    pass


class ID(BigqueryNode):
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

    @root_validator(pre=True)
    def make_full_name(cls, values: Dict) -> Dict:
        """

        Args:
            values (Dict):

        Returns:

        Raises:

        """
        if values.get("full_name", None) is None:
            values["full_name"] = f"{values['table_schema']}.{values['name']}"
        return values


class ColumnID(ID):
    """ """

    table_schema: str
    table_name: str

    @root_validator(pre=True)
    def make_full_name(cls, values: Dict) -> Dict:
        """

        Args:
            values (Dict):

        Returns:

        Raises:

        """
        full_name = values.get("full_name", None)
        if values.get("full_name", None) is None:
            values["full_name"] = f"{values['table_schema']}.{values['table_name']}.{values['name']}"
        return values

    @validator("table_name")
    def validate_name(cls, value):
        """

        Args:
            value:

        Returns:

        Raises:

        """
        if value.startswith('"') and value.endswith('"'):
            return value
        return value.lower()


class Column(BigqueryNode):
    """ """

    name: str = Field(alias="column_name")
    table: str
    column_schema: str = Field(alias="schema")
    data_type: str
    is_nullable: bool
    namespace: str
    default_value: Any = Field(alias="column_default")
    is_pk: Optional[bool]
    full_name: Optional[str] = None

    class Config:
        """ """

        allow_population_by_field_name = True

    @validator("full_name", always=True)
    def make_full_name(cls, full_name: Optional[str], values: Dict) -> str:
        """

        Args:
            full_name (Optional[str]):
            values (Dict):

        Returns:

        Raises:

        """
        if full_name is not None:
            return full_name
        result = f"{values['column_schema']}.{values['table']}.{values['name']}"
        return result

    @validator("name")
    def validate_name(cls, value):
        """

        Args:
            value:

        Returns:

        Raises:

        """
        if value.startswith('"') and value.endswith('"'):
            return value
        return value.lower()


class Constraint(str, Enum):
    """ """

    foreign_key = "f"
    primary_key = "p"
    belongs_to = "bt"
    bigquery_model = "bqm"


class Edge(BaseModel):
    """ """

    source: Union[ColumnID, TableID]
    destination: Union[ColumnID, TableID]
    definition: Optional[str]
    constraint_type: Constraint
    metadata: Optional[Dict] = None

    def __hash__(self):
        """

        Returns:

        Raises:

        """
        return hash(
            (
                (self.source.namespace, self.source.full_name),
                (self.destination.namespace, self.destination.full_name),
            )
        )


class TableType(str, Enum):
    """ """

    Table = "BASE TABLE"
    Clone = "CLONE"
    Snapshot = "SNAPSHOT"
    View = "VIEW"
    Materialized_View = "MATERIALIZED VIEW"
    External = "EXTERNAL"


class Table(BigqueryNode):
    """ """

    name: str = Field(alias="table_name")
    table_schema: str = Field(alias="schema")
    table_type: TableType
    table_dataset: str
    namespace: str
    columns: List[Column] = []
    metadata: Dict = {}
    full_name: Optional[str] = None

    class Config:
        """ """

        allow_population_by_field_name = True

    @validator("full_name", always=True)
    def make_full_name(cls, full_name: Optional[str], values: Dict) -> str:
        """

        Args:
            full_name (Optional[str]):
            values (Dict):

        Returns:

        Raises:

        """
        if full_name is not None:
            return full_name

        return f"{values['table_schema']}.{values['name']}"

    @validator("name")
    def validate_name(cls, value):
        """

        Args:
            value:

        Returns:

        Raises:

        """
        if value.startswith('"') and value.endswith('"'):
            return value
        return value.lower()

    def get_edges(self) -> List[Edge]:
        """

        Args:

        Returns:

        Raises:

        """
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
    self_columns: List[str]
    foreign_schema: str
    foreign_table: str
    foreign_columns: List[str]
    definition: str

    def to_edge(self) -> Optional[Edge]:
        """

        Args:

        Returns:

        Raises:

        """
        if not len(self.self_columns) == 1 and len(self.foreign_columns) == 1:
            return None

        destination = ColumnID(
            table_schema=self.self_schema,
            table_name=self.self_table,
            name=self.self_columns[0],
            namespace=self.namespace,
        )
        source = ColumnID(
            table_schema=self.foreign_schema,
            table_name=self.foreign_table,
            name=self.foreign_columns[0],
            namespace=self.namespace,
        )
        return Edge(
            definition=self.definition,
            source=source,
            destination=destination,
            constraint_type=self.constraint_type,
        )
