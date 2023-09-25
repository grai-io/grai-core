from typing import Dict, Literal, Union

from grai_schemas.base import GraiType
from grai_schemas.generics import GraiBaseModel


class Schema(GraiBaseModel):
    """Class definition of Schema

    Attributes:
        entity: todo

    """

    entity: GraiType

    @classmethod
    def to_model(cls, item: Dict, version: Literal["v1"], typing_type: Literal["Node", "Edge"]) -> GraiType:
        """

        Args:
            item (Dict):
            version (Literal["v1"]):
            typing_type (Literal["Node", "Edge"]):

        Returns:

        Raises:

        """
        result = {
            "type": typing_type,
            "version": version,
            "spec": item,
        }
        return cls(entity=result).entity
