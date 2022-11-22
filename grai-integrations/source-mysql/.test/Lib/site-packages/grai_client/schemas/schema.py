from pathlib import Path
from typing import Any, Dict, Iterable, Type, Union

import yaml
from grai_client.schemas.edge import Edge
from grai_client.schemas.node import Node
from grai_client.schemas.utilities import GraiBaseModel
from pydantic import Field
from typing_extensions import Annotated

GraiType = Annotated[Union[Node, Edge], Field(discriminator="type")]


class Schema(GraiBaseModel):
    entity: GraiType

    @classmethod
    def to_model(cls, item: Dict, version: str, typing_type: str) -> GraiType:
        result = {
            "type": typing_type,
            "version": version,
            "spec": item,
        }
        return cls(entity=result).entity


def validate_file(file: Union[str, Path]) -> Iterable[GraiType]:
    with open(file) as f:
        for item in yaml.safe_load_all(f):
            yield Schema(entity=item).entity
