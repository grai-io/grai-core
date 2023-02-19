from functools import cached_property
from itertools import chain
from typing import List, Union

from dbt_artifacts_parser.parsers.manifest.manifest_v5 import (
    CompiledAnalysisNode,
    CompiledGenericTestNode,
    CompiledHookNode,
    CompiledModelNode,
    CompiledRPCNode,
    CompiledSeedNode,
    CompiledSingularTestNode,
    CompiledSnapshotNode,
    CompiledSqlNode,
    ManifestV5,
    ParsedAnalysisNode,
    ParsedGenericTestNode,
    ParsedHookNode,
    ParsedModelNode,
    ParsedRPCNode,
    ParsedSeedNode,
    ParsedSingularTestNode,
    ParsedSnapshotNode,
    ParsedSourceDefinition,
    ParsedSqlNode,
)

from grai_source_dbt.models.nodes import Column, Edge, EdgeTerminus
from grai_source_dbt.models.shared import Constraint
from grai_source_dbt.utils import full_name
from grai_source_dbt.versions.base import BaseManifestLoader
from grai_source_dbt.versions.utils import DbtTypes

V5NodeTypes = Union[
    CompiledAnalysisNode,
    CompiledSingularTestNode,
    CompiledModelNode,
    CompiledHookNode,
    CompiledRPCNode,
    CompiledSqlNode,
    CompiledGenericTestNode,
    CompiledSeedNode,
    CompiledSnapshotNode,
    ParsedAnalysisNode,
    ParsedSingularTestNode,
    ParsedHookNode,
    ParsedModelNode,
    ParsedRPCNode,
    ParsedSqlNode,
    ParsedGenericTestNode,
    ParsedSeedNode,
    ParsedSnapshotNode,
]

DbtTypes.register_nodes(V5NodeTypes)
DbtTypes.register_all(ParsedSourceDefinition)
DbtTypes.register_manifest(ManifestV5)


@full_name.register
def node_full_name(obj: V5NodeTypes):
    return f"{obj.schema_}.{obj.name}"


@full_name.register
def source_full_name(obj: ParsedSourceDefinition):
    return f"{obj.schema_}.{obj.identifier}"


class ManifestLoaderV5(BaseManifestLoader):
    manifest: ManifestV5

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

    @property
    def edges(self) -> List[Edge]:
        def get_edges():
            for table in self.node_map.values():
                for column in table.columns.values():
                    column = self.columns[(table.unique_id, column.name)]
                    edge = Edge(
                        constraint_type=Constraint("bt"),
                        source=EdgeTerminus(name=full_name(table), namespace=self.namespace),
                        destination=EdgeTerminus(name=full_name(column), namespace=self.namespace),
                    )
                    yield edge
                if hasattr(table, "depends_on"):
                    for parent_str in table.depends_on.nodes:
                        source_node = self.node_map[parent_str]
                        edge = Edge(
                            constraint_type=Constraint("dbtm"),
                            source=EdgeTerminus(name=full_name(source_node), namespace=self.namespace),
                            destination=EdgeTerminus(name=full_name(table), namespace=self.namespace),
                            definition=self.node_map[parent_str].raw_sql,
                        )
                        yield edge

        return list(get_edges())
