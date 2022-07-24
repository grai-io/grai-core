from pathlib import Path
from typing import Any, Dict, Iterable, Type, Union

import yaml
from grai_client.schemas.edge import Edge, EdgeType
from grai_client.schemas.node import Node, NodeType
from grai_client.schemas.utilities import DispatchType
from multimethod import multimethod
from pydantic import BaseModel, Field
from typing_extensions import Annotated

GraiType = Annotated[Union[Node, Edge], Field(discriminator="type")]


class Schema(BaseModel):
    entity: GraiType

    @classmethod
    def to_model(cls, item: Dict, version: str, typing_type: DispatchType) -> GraiType:
        result = {
            "type": typing_type.type,
            "version": version,
            "spec": item,
        }
        return cls(entity=result).entity


def validate_file(file: Union[str, Path]) -> Iterable[GraiType]:
    with open(file) as f:
        for item in yaml.safe_load_all(f):
            yield Schema(entity=item).entity
