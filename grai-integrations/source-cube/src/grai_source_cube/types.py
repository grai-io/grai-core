from typing import List, Optional, Union

from grai_source_cube.api import CubeSchema, DimensionSchema, MeasureSchema
from pydantic import BaseModel


class GraiID(BaseModel):
    name: str
    namespace: str
    display_name: Optional[str]


class SourceNode(BaseModel):
    node_id: GraiID
    metadata: BaseModel = BaseModel()

    @staticmethod
    def edges() -> List["CubeEdge"]:
        return []


class SourceTableNode(SourceNode):
    pass


class SourceColumnNode(SourceNode):
    pass


class CubeNode(BaseModel):
    node_id: GraiID
    metadata: CubeSchema
    source_node: Optional[SourceNode]

    @classmethod
    def from_schema(cls, cube: CubeSchema, namespace: str, source: Optional[SourceNode]) -> "CubeNode":
        return cls(
            node_id=GraiID(name=cube.name, namespace=namespace),
            metadata=cube,
            source_node=source,
        )

    def edges(self) -> List["CubeEdge"]:
        # source -> cube
        if self.source_node is None:
            return []
        return [CubeEdge(source=self.source_node, destination=self)]


class DimensionNode(BaseModel):
    node_id: GraiID
    cube_ref: CubeNode
    metadata: DimensionSchema

    @classmethod
    def from_schema(cls, dimension: DimensionSchema, cube: CubeNode) -> "DimensionNode":
        return cls(
            node_id=GraiID(name=f"{cube.node_id.name}.{dimension.name}", namespace=cube.node_id.namespace),
            cube_ref=cube,
            metadata=dimension,
        )

    def edges(self) -> List["CubeEdge"]:
        # source -> dimension
        # dimension -> source
        return [
            CubeEdge(source=self.cube_ref, destination=self)
            # TODO: Add source column -> dimension
        ]


class MeasureNode(BaseModel):
    node_id: GraiID
    cube_ref: CubeNode
    metadata: MeasureSchema

    @classmethod
    def from_schema(cls, measure: MeasureSchema, cube: CubeNode) -> "MeasureNode":
        return cls(
            node_id=GraiID(name=f"{cube.node_id.name}.{measure.name}", namespace=cube.node_id.namespace),
            cube_ref=cube,
            metadata=measure,
        )

    def edges(self) -> List["CubeEdge"]:
        # source -> measure
        # measure -> source
        return [
            CubeEdge(source=self.cube_ref, destination=self)
            # TODO: Add source -> measure
        ]


class CubeEdge(BaseModel):
    source: Union[MeasureNode, DimensionNode, CubeNode, SourceNode]
    destination: Union[MeasureNode, DimensionNode, CubeNode, SourceNode]


class CubeEdgeUnionFiller(CubeEdge):
    # this is just to stick the Edge Types in a Union
    pass


CubeNodeTypes = Union[CubeNode, DimensionNode, MeasureNode, SourceNode]
CubeEdgeTypes = Union[CubeEdge, CubeEdgeUnionFiller]
