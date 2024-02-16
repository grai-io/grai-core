from typing import Union

from api import CubeSchema, DimensionSchema, MeasureSchema
from pydantic import BaseModel


class GraiID(BaseModel):
    name: str
    namespace: str


class CubeNode(BaseModel):
    source_table: GraiID
    node: Union[DimensionSchema, MeasureSchema]


class CubeEdge(BaseModel):
    source: GraiID
    destination: GraiID
    metadata: CubeSchema
