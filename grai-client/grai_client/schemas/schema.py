from pathlib import Path
from typing import Any, Dict, Iterable, Literal, Type, Union

import yaml
from pydantic import Field
from typing_extensions import Annotated

from grai_client.schemas.edge import Edge
from grai_client.schemas.node import Node
from grai_client.schemas.utilities import GraiBaseModel

GraiType = Annotated[Union[Node, Edge], Field(discriminator="type")]


class Schema(GraiBaseModel):
    entity: GraiType

    @classmethod
    def to_model(
        cls, item: Dict, version: Literal["v1"], typing_type: Literal["Node", "Edge"]
    ) -> GraiType:
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
