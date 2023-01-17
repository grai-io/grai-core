from typing import Union

from grai_schemas.models import GraiEdgeMetadata, GraiNodeMetadata
from pydantic import BaseModel


class Metadata(BaseModel):
    grai: Union[GraiNodeMetadata, GraiEdgeMetadata]
