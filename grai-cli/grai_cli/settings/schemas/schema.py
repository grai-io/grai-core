from typing import Iterable, Union, Type
from pydantic import BaseModel, Field
from grai_cli.settings.schemas.edge import Edge, EdgeType
from grai_cli.settings.schemas.node import Node, NodeType
from typing_extensions import Annotated
from grai_cli.utilities.utilities import load_all_yaml
from pathlib import Path


GraiType = Annotated[Union[Node, Edge], Field(discriminator='type')]


class Schema(BaseModel):
    entity: GraiType


class SchemaGenericTypes:
    node = NodeType()
    edge = EdgeType()


def validate_file(file: str | Path) -> Iterable[Type[GraiType]]:
    for config in load_all_yaml(file):
        yield Schema(entity=config).entity
