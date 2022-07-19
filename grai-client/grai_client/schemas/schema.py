from typing import Iterable, Union, Type, Dict
from pydantic import BaseModel, Field
from grai_client.schemas.edge import Edge, EdgeType
from grai_client.schemas.node import Node, NodeType
from typing_extensions import Annotated
import yaml
from pathlib import Path


GraiType = Annotated[Union[Node, Edge], Field(discriminator="type")]


class Schema(BaseModel):
    entity: GraiType

    @classmethod
    def to_model(cls, item: Dict, version: str, type: str):
        result = {
            "type": type,
            "version": version,
            "spec": item,
        }
        return cls(entity=result).entity


def validate_file(file: str | Path) -> Iterable[Type[GraiType]]:
    with open(file) as f:
        for item in yaml.safe_load_all(f):
            yield Schema(entity=item).entity


class SchemaGenericTypes:
    node: Node = NodeType()
    edge: Edge = EdgeType()
