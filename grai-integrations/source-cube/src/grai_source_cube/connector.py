import itertools
from functools import cached_property
from typing import Dict, List

from grai_source_cube.api import CubeAPI, CubeSchema
from grai_source_cube.settings import CubeApiConfig
from grai_source_cube.types import (
    CubeEdgeTypes,
    CubeNode,
    CubeNodeTypes,
    DimensionNode,
    GraiID,
    MeasureNode,
    SourceNode,
)
from pydantic import BaseModel


class CubeSourceMap(BaseModel):
    map: Dict[str, GraiID] = {}


class CubeConnector(CubeAPI):
    """ """

    def __init__(self, namespace_map: Dict[str, GraiID], config: CubeApiConfig, *args, **kwargs):
        self.source_map = CubeSourceMap(map=namespace_map).map
        super().__init__(config=config)

    def get_cube_source(self, cube: CubeSchema) -> SourceNode:
        if cube.name in self.source_map:
            cube_source = self.source_map[cube.name]
        elif cube.grai_meta is not None:
            cube_id = GraiID(name=cube.grai_meta.table_name, namespace=cube.grai_meta.namespace)
            cube_source = SourceNode(node_id=cube_id)
        else:
            raise Exception(f"Cube {cube.name} does not have a source map or associated grai metadata")

        return cube_source

    @cached_property
    def cubes(self) -> List[CubeSchema]:
        return self.meta().cubes

    @cached_property
    def nodes(self) -> List[CubeNodeTypes]:
        # Need to identify the source table, and columns from sql
        # Nodes will include, source table, source column, cube measures, and cube dimensions
        nodes = []
        for cube in self.cubes:
            cube_node = CubeNode.from_schema(cube)
            source_table = self.get_cube_source(cube)
            # source_columns = ...
            measures = (MeasureNode.from_schema(measure, cube_node) for measure in cube.measures)
            dimensions = (DimensionNode.from_schema(dimension, cube_node) for dimension in cube.dimensions)
            nodes.extend(itertools.chain([cube_node, source_table], measures, dimensions))
        return nodes

    @cached_property
    def edges(self) -> List[CubeEdgeTypes]:
        # Edges between source columns and cube measures / dimensions
        edge_iters = (node.edges() for node in self.nodes)
        edges = list(itertools.chain(*edge_iters))
        return edges
