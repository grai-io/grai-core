from typing import Dict, Literal, Union

from grai_schemas.base import GraiType
from grai_schemas.generics import GraiBaseModel


class Schema(GraiBaseModel):
    """Class definition of Schema

    Attributes:
        entity: A Grai object

    """

    entity: GraiType

    @classmethod
    def to_model(cls, item: Dict, version: Literal["v1"], typing_type: Literal["Node", "Edge"]) -> GraiType:
        """Convert an item spec to a Grai object

        Args:
            item: An item spec to be converted to a Grai object
            version: which version of the schema to use
            typing_type: The type of the object e.g. Node, Edge, etc.

        Returns:
            The Grai object

        Raises:

        """
        result = {
            "type": typing_type,
            "version": version,
            "spec": item,
        }
        return cls(entity=result).entity
