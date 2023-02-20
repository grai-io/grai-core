from functools import cached_property
from itertools import chain
from typing import List, Type, Union, get_args

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

set_extra_fields([*get_args(NodeTypes), SourceTypes])


class ManifestLoaderV1(BaseManifestLoader):
    @cached_property
    def test_resources(self):
        test_gen = (test for test in self.manifest.nodes.values() if test.resource_type.value == "test")
        col_to_tests = {}
        for test in test_gen:
            if getattr(test, "column_name", None) is not None:
                for node_id in test.depends_on.nodes:
                    unique_id = (node_id, test.column_name)
                    col_to_tests.setdefault(unique_id, [])
                    col_to_tests[unique_id].append(test)
        return col_to_tests

    @cached_property
    def node_map(self):
        node_resource_types = {"model", "seed"}
        node_map = {
            node_id: node
            for node_id, node in self.manifest.nodes.items()
            if node.resource_type.value in node_resource_types
        }
        node_map.update(self.manifest.sources)
        return node_map

    @cached_property
    def columns(self):
        columns = {}
        for node in self.node_map.values():
            for column in node.columns.values():
                column = Column.from_table_column(node, column, self.namespace)
                if column.unique_id in self.test_resources:
                    column.tests = self.test_resources[column.unique_id]
                columns[column.unique_id] = column
        return columns

    @property
    def nodes(self) -> List:
        nodes = list(chain(self.node_map.values(), self.columns.values()))
        return list(nodes)

    def make_edge(self, source, destination, constraint_type, definition: bool = False) -> Edge:
        source_terminus = EdgeTerminus(name=full_name(source), namespace=self.namespace)
        destination_terminus = EdgeTerminus(name=full_name(destination), namespace=self.namespace)
        if definition:
            return Edge(
                constraint_type=constraint_type,
                source=source_terminus,
                destination=destination_terminus,
                definition=source.raw_sql,
            )
        else:
            return Edge(
                constraint_type=constraint_type,
                source=source_terminus,
                destination=destination_terminus,
            )

    @property
    def edges(self) -> List[Edge]:
        def get_edges():
            for table in self.node_map.values():
                for column in table.columns.values():
                    column = self.columns[(table.unique_id, column.name)]
                    edge = self.make_edge(table, column, Constraint("bt"))
                    yield edge
                if hasattr(table, "depends_on"):
                    for parent_str in table.depends_on.nodes:
                        source_node = self.node_map[parent_str]
                        edge = self.make_edge(source_node, table, Constraint("dbtm"), True)
                        yield edge

        return list(get_edges())
