from functools import cached_property
from itertools import chain
from typing import Dict, List, Tuple, Type, TypeVar, Union, get_args

from dbt_artifacts_parser.parsers.manifest.manifest_v1 import (
    CompiledAnalysisNode,
    CompiledDataTestNode,
    CompiledHookNode,
    CompiledModelNode,
    CompiledRPCNode,
    CompiledSchemaTestNode,
    CompiledSeedNode,
    CompiledSnapshotNode,
    ManifestV1,
    ParsedAnalysisNode,
    ParsedDataTestNode,
    ParsedHookNode,
    ParsedModelNode,
    ParsedRPCNode,
    ParsedSchemaTestNode,
    ParsedSeedNode,
    ParsedSnapshotNode,
    ParsedSourceDefinition,
)
from grai_schemas.v1.metadata.edges import EdgeTypeLabels

from grai_source_dbt.loaders.base import BaseManifestLoader
from grai_source_dbt.models.grai import Column, Edge, EdgeTerminus
from grai_source_dbt.models.shared import Constraint
from grai_source_dbt.utils import full_name, set_extra_fields

NodeTypes = Union[
    CompiledAnalysisNode,
    CompiledDataTestNode,
    CompiledModelNode,
    CompiledHookNode,
    CompiledRPCNode,
    CompiledSchemaTestNode,
    CompiledSeedNode,
    CompiledSnapshotNode,
    ParsedAnalysisNode,
    ParsedDataTestNode,
    ParsedHookNode,
    ParsedModelNode,
    ParsedRPCNode,
    ParsedSchemaTestNode,
    ParsedSeedNode,
    ParsedSnapshotNode,
    ParsedSnapshotNode,
]
SourceTypes = Union[ParsedSourceDefinition]


TestType = Union[ParsedDataTestNode, CompiledDataTestNode, CompiledSchemaTestNode, ParsedSchemaTestNode]
ColumnType = TypeVar("ColumnType")
NodeType = TypeVar("NodeType")
DBTNodeType = TypeVar("DBTNodeType")


class ManifestLoaderV1(BaseManifestLoader):
    @cached_property
    def test_resources(self) -> Dict[Tuple[str, str], List[TestType]]:
        test_gen = (test for test in self.manifest.nodes.values() if test.resource_type == "test")
        col_to_tests: Dict[Tuple[str, str], List[TestType]] = dict()
        for test in test_gen:
            if getattr(test, "column_name", None) is not None:
                for node_id in test.depends_on.nodes:
                    unique_id = (node_id, test.column_name)
                    col_to_tests.setdefault(unique_id, [])
                    col_to_tests[unique_id].append(test)
        return col_to_tests

    @cached_property
    def node_map(self) -> Dict[str, DBTNodeType]:
        node_resource_types = {"model", "seed"}
        node_map = {
            node_id: node for node_id, node in self.manifest.nodes.items() if node.resource_type in node_resource_types
        }
        return node_map

    @cached_property
    def columns(self) -> Dict[Tuple[str, str], ColumnType]:
        columns = {}
        for node in chain(self.node_map.values(), self.manifest.sources.values()):
            for column in node.columns.values():
                column = Column.from_table_column(node, column, self.namespace)
                if column.unique_id in self.test_resources:
                    column.tests = self.test_resources[column.unique_id]
                columns[column.unique_id] = column
        return columns

    @property
    def nodes(self) -> List[NodeType]:
        nodes = list(chain(self.node_map.values(), self.columns.values(), self.manifest.sources.values()))
        return list(nodes)

    def make_edge(self, source, destination, constraint_type, edge_type, definition: bool = False) -> Edge:
        source_terminus = EdgeTerminus(name=full_name(source), namespace=self.namespace)
        destination_terminus = EdgeTerminus(name=full_name(destination), namespace=self.namespace)
        if definition:
            return Edge(
                constraint_type=constraint_type,
                source=source_terminus,
                destination=destination_terminus,
                definition=destination.compiled_sql if hasattr(destination, "compiled_sql") else destination.raw_sql,
                edge_type=edge_type,
            )
        else:
            return Edge(
                constraint_type=constraint_type,
                source=source_terminus,
                destination=destination_terminus,
                edge_type=edge_type,
            )

    @property
    def edges(self) -> List[Edge]:
        result = []
        for table in self.node_map.values():
            for column in table.columns.values():
                column = self.columns[(table.unique_id, column.name)]
                edge = self.make_edge(table, column, Constraint("bt"), EdgeTypeLabels.table_to_column)
                result.append(edge)

            # Seeds don't have depends_on and will error without this check.
            if hasattr(table.depends_on, "nodes"):
                for parent_str in table.depends_on.nodes:
                    source_node = (
                        self.node_map[parent_str] if parent_str in self.node_map else self.manifest.sources[parent_str]
                    )
                    edge = self.make_edge(source_node, table, Constraint("dbtm"), EdgeTypeLabels.table_to_table, True)
                    result.append(edge)

        for table in self.manifest.sources.values():
            for column in table.columns.values():
                column = self.columns[(table.unique_id, column.name)]
                edge = self.make_edge(table, column, Constraint("bt"), EdgeTypeLabels.table_to_column)
                result.append(edge)
        return result
