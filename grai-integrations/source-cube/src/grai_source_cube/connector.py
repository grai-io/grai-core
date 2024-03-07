import itertools
from functools import cached_property
from typing import Dict, List, Optional

from grai_source_cube.api import CubeAPI, CubeSchema
from grai_source_cube.settings import CubeApiConfig
from grai_source_cube.types import (
    CubeEdgeTypes,
    CubeNode,
    CubeNodeTypes,
    DimensionNode,
    GraiID,
    MeasureNode,
    SourceTableNode,
)
from pydantic import BaseModel


class NamespaceMap(BaseModel):
    map: Dict[str, str] = {}


class CubeConnector(CubeAPI):
    """ """

    def __init__(self, namespace: str, config: CubeApiConfig, *args, **kwargs):
        self.namespace = namespace
        super().__init__(config=config)

    @staticmethod
    def get_cube_source_table(cube: CubeSchema) -> Optional[SourceTableNode]:
        if cube.meta.grai is None:
            return None

        if cube.meta.grai.table_name is None:
            # TODO: We should extract this from the sql
            return None
        else:
            table_name = cube.meta.grai.table_name
        cube_id = GraiID(name=table_name, namespace=cube.meta.grai.data_source_namespace)
        cube_source = SourceTableNode(node_id=cube_id)
        return cube_source

    @cached_property
    def cubes(self) -> List[CubeSchema]:
        cubes = self.meta().cubes
        return cubes

    @cached_property
    def nodes(self) -> List[CubeNodeTypes]:
        # Need to identify the source table, and columns from sql
        # Nodes will include, source table, source column, cube measures, and cube dimensions
        nodes = []
        for cube in self.cubes:
            source_table = self.get_cube_source_table(cube)
            cube_node = CubeNode.from_schema(cube, self.namespace, source_table)

            # source_columns = ...
            initial_nodes = [cube_node] if source_table is None else [cube_node, source_table]
            measures = (MeasureNode.from_schema(measure, cube_node) for measure in cube.measures)
            dimensions = (DimensionNode.from_schema(dimension, cube_node) for dimension in cube.dimensions)
            nodes.extend(itertools.chain(initial_nodes, measures, dimensions))
        return nodes

    @cached_property
    def edges(self) -> List[CubeEdgeTypes]:
        # Edges between source columns and cube measures / dimensions
        edge_iters = (node.edges() for node in self.nodes)
        edges = list(itertools.chain(*edge_iters))
        return edges
