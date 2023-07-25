from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class ID(BaseModel):
    """ """

    name: str
    namespace: str
    # full_name: str


class Table(ID):
    """ """

    file_name: str
    columns: Optional[List["Column"]] = None

    @property
    def full_name(self):
        """ """
        return self.name

    def get_edges(self) -> List["Edge"]:
        """

        Args:

        Returns:

        Raises:

        """
        if self.columns is None:
            return []

        return [Edge(source=self, destination=column) for column in self.columns]


class Column(ID):
    """ """

    name: str = Field(alias="column_name")
    namespace: str
    table: str
    data_type: str
    is_nullable: bool

    class Config:
        """ """

        allow_population_by_field_name = True

    @property
    def full_name(self):
        """ """
        return f"{self.table}.{self.name}"


class Edge(BaseModel):
    """ """

    source: Union[Table, Column]
    destination: Union[Table, Column]
    constraint_type: Literal["bt"] = "bt"
