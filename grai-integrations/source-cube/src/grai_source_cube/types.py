from typing import List, Optional, Union

from grai_source_cube.api import CubeSchema, DimensionSchema, MeasureSchema
from pydantic import BaseModel


class GraiID(BaseModel):
    name: str
    namespace: str
    display_name: Optional[str]


class BaseNode(BaseModel):
    node_id: GraiID
    metadata: BaseModel


class SourceNode(BaseNode):
    node_id: GraiID
    metadata: BaseModel = BaseModel()

    @staticmethod
    def edges() -> List["CubeEdge"]:
        return []


class SourceTableNode(SourceNode):
    pass


class SourceColumnNode(SourceNode):
    pass


class CubeNode(BaseNode):
    node_id: GraiID
    metadata: CubeSchema
    source_node: Optional[SourceTableNode]

    @classmethod
    def from_schema(cls, cube: CubeSchema, namespace: str, source: Optional[SourceNode]) -> "CubeNode":
        return cls(
            node_id=GraiID(name=cube.name, namespace=namespace),
            metadata=cube,
            source_node=source,
        )

    def edges(self) -> List["CubeEdgeTableToTable"]:
        # source -> cube
        if self.source_node is None:
            return []

        return [CubeEdgeTableToTable(source=self.source_node, destination=self)]


class DimensionNode(BaseNode):
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

    def edges(self) -> List["CubeEdgeTableToColumn"]:
        # source -> dimension
        # dimension -> source
        return [
            CubeEdgeTableToColumn(source=self.cube_ref, destination=self)
            # TODO: Add source column -> dimension
        ]


class MeasureNode(BaseNode):
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

    def edges(self) -> List["CubeEdgeTableToColumn"]:
        # source -> measure
        # measure -> source
        return [
            CubeEdgeTableToColumn(source=self.cube_ref, destination=self)
            # TODO: Add source -> measure
        ]


class BaseCubeEdge(BaseModel):
    source: BaseNode
    destination: BaseNode


class CubeEdgeTableToColumn(BaseCubeEdge):
    source: Union[CubeNode, SourceTableNode]
    destination: Union[MeasureNode, DimensionNode, SourceColumnNode]


class CubeEdgeTableToTable(BaseCubeEdge):
    source: Union[CubeNode, SourceTableNode]
    destination: Union[CubeNode, SourceTableNode]


class CubeEdgeColumnToColumn(BaseCubeEdge):
    source: Union[SourceColumnNode, MeasureNode, DimensionNode]
    destination: Union[SourceColumnNode, MeasureNode, DimensionNode]


CubeNodeTypes = Union[CubeNode, DimensionNode, MeasureNode, SourceTableNode, SourceColumnNode]
CubeEdgeTypes = Union[CubeEdgeTableToColumn, CubeEdgeTableToTable, CubeEdgeColumnToColumn]
