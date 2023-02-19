import json
from abc import ABC, abstractmethod
from functools import cached_property
from itertools import chain
from typing import Dict, List, Protocol, Tuple, Union

from dbt_artifacts_parser.parser import parse_manifest
from dbt_artifacts_parser.parsers.manifest.manifest_v5 import ManifestV5
from dbt_artifacts_parser.parsers.utils import get_dbt_schema_version
from dbt_artifacts_parser.parsers.version_map import ArtifactTypes

from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.models.nodes import Column, Edge, EdgeTerminus
from grai_source_dbt.models.shared import Constraint
from grai_source_dbt.versions import full_name
from grai_source_dbt.versions.v5 import GraiExtras


class BaseManifestLoader(ABC):
    def __init__(self, manifest, namespace):
        self.manifest = manifest
        self.namespace = namespace


class BaseLoaderMixin(ABC):
    manifest: ManifestV5
    namespace: str

    def __init__(self, manifest, namespace, *args, **kwargs):
        self.manifest = manifest
        self.namespace = namespace

        for node in self.manifest.nodes.values():
            node.grai_ = GraiExtras(full_name=full_name(node), namespace=self.namespace)
        for node in self.manifest.sources.values():
            node.grai_ = GraiExtras(full_name=full_name(node), namespace=self.namespace)

    # @abstractmethod
    # def process_manifest(self) -> Tuple[List, List]:
    #     raise NotImplementedError

    @property
    @abstractmethod
    def nodes(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def edges(self):
        raise NotImplementedError

    @property
    def adapted_nodes(self):
        return adapt_to_client(self.nodes, "v1")

    @property
    def adapted_edges(self):
        return adapt_to_client(self.edges, "v1")


class LoaderV5Mixin(BaseLoaderMixin):
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


class ManifestLoaderV5(LoaderV5Mixin):
    pass


class Manifest(BaseManifestLoader):
    manifest_map = {ArtifactTypes.MANIFEST_V5.value.dbt_schema_version: ManifestLoaderV5}

    @classmethod
    def load(cls, file: str, namespace: str):
        with open(file, "r") as f:
            manifest_dict = json.load(f)

        version = get_dbt_schema_version(manifest_dict)
        if version not in cls.manifest_map:
            message = f"Manifest version {version} not yet supported"
            raise NotImplementedError(message)

        manifest = parse_manifest(manifest_dict)
        return cls.manifest_map[version](manifest, namespace)
