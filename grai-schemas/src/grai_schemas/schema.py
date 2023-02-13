from typing import Dict, Literal, Union

from grai_schemas.base import Edge, Node
from grai_schemas.generics import GraiBaseModel

GraiType = Union[Node, Edge]


class Schema(GraiBaseModel):
    entity: GraiType

    @classmethod
    def to_model(cls, item: Dict, version: Literal["v1"], typing_type: Literal["Node", "Edge"]) -> GraiType:
        result = {
            "type": typing_type,
            "version": version,
            "spec": item,
        }
        return cls(entity=result).entity
