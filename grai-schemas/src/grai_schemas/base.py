from typing import Union

from grai_schemas.models import GraiEdgeMetadata, GraiNodeMetadata
from pydantic import BaseModel


class EdgeMetadata(BaseModel):
    grai: GraiEdgeMetadata


class NodeMetadata(BaseModel):
    grai: GraiNodeMetadata


__all__ = ["EdgeMetadata", "NodeMetadata"]
