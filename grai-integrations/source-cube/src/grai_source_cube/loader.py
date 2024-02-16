from functools import cached_property
from itertools import chain
from typing import Dict, List, Tuple

from pydantic import BaseModel

from grai_source_cube.api import CubeAPI, CubeSchema, DimensionSchema, MeasureSchema
from grai_source_cube.configs import CubeApiConfig
from grai_source_cube.types import CubeNode, GraiID


class CubeSourceMap(BaseModel):
    map: Dict[str, GraiID]


class CubeConnector(CubeAPI):
    """ """

    def __init__(self, namespace_map: Dict[str, GraiID], config: CubeApiConfig, *args, **kwargs):
        self.source_map = CubeSourceMap(map=namespace_map).map
        super().__init__(config=config)

    def get_cube_source(self, cube: CubeSchema) -> GraiID:
        if cube.name in self.source_map:
            cube_source = self.source_map[cube.name]
        elif cube.meta.grai is not None:
            cube_source = GraiID(name=cube.meta.grai.table_name, namespace=cube.meta.grai.namespace)
        else:
            raise Exception(f"Cube {cube.name} does not have a source map or associated grai metadata")

        return cube_source

    @cached_property
    def cubes(self) -> List[CubeSchema]:
        return self.call_meta().cubes

    def nodes(self) -> List[CubeNode]:
        # Need to identify the source table, and columns from sql
        # Nodes will include, source table, source column, cube measures, and cube dimensions
        nodes = []
        for cube in self.cubes:
            cube_source = self.get_cube_source(cube)

            nodes.extend(
                [CubeNode(source_table=cube_source, node=cube_obj) for cube_obj in (*cube.measures, *cube.dimensions)]
            )
        return nodes

    def edges(self) -> List[CubeNode]:
        # Edges between source columns and cube measures / dimensions
        pass
