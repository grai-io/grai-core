from abc import ABC, abstractmethod
from itertools import chain
from typing import Dict, List

from grai_graph.analysis import Graph, GraphAnalyzer
from grai_schemas.v1 import EdgeV1, NodeV1
from connections.task_helpers import schemaToModel
from lineage.models import Node

SEPARATOR_CHAR = "/"


def build_node_name(node: NodeV1) -> str:
    return f"{node.spec.namespace}{SEPARATOR_CHAR}{node.spec.name}"


class TestResult(ABC):
    """Assumed to be a failing test result"""

    type: str

    def __init__(self, node: NodeV1, test_path: List[NodeV1]):
        self.node = node
        self.failing_node = test_path[-1]
        self.test_path = test_path
        self.node_name = build_node_name(self.node)
        self.failing_node_name = build_node_name(self.failing_node)

    @abstractmethod
    def message(self) -> str:
        return ""

    def make_row(self) -> str:
        row = f"| {self.node.spec.namespace} | {self.node.spec.name} | {self.failing_node_name} | {self.type} | {self.message()} |"
        return row

    def error_metadata(self) -> Dict:
        return {
            "source": self.node.spec.name,
            "destination": self.failing_node.spec.name,
            "type": self.type,
            "message": self.message(),
        }

    def nodeToJson(self, node):
        return {"id": str(node.spec.id), "name": node.spec.name, "namespace": node.spec.namespace}

    def toJSON(self):
        return {
            "type": self.type,
            "node": self.nodeToJson(self.node),
            "failing_node": self.nodeToJson(self.failing_node),
            "node_name": self.node_name,
            "failing_node_name": self.failing_node_name,
        }  # "test_path": self.test_path


class TypeTestResult(TestResult):
    type = "Data Type"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.data_type
        self.provided_value = self.node.spec.metadata.grai.node_attributes.data_type

    def message(self) -> str:
        return f"Node `{self.failing_node_name}` expected to be {self.expected_value} not {self.provided_value}"


class UniqueTestResult(TestResult):
    type = "Uniqueness"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.is_unique
        self.provided_value = self.node.spec.metadata.grai.node_attributes.is_unique

    def message(self) -> str:
        to_be_or_not_to_be = "not " if self.expected_value else ""
        return f"Node `{self.failing_node_name}` expected {to_be_or_not_to_be}to be unique"


class NullableTestResult(TestResult):
    type = "Nullable"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_value = self.failing_node.spec.metadata.grai.node_attributes.is_nullable
        self.provided_value = self.node.spec.metadata.grai.node_attributes.is_nullable

    def message(self) -> str:
        to_be_or_not_to_be = "not " if self.expected_value else ""
        return f"Node `{self.failing_node_name}` expected {to_be_or_not_to_be}to be nullable"


class TestResultCacheBase:
    def __init__(self, new_nodes: List[NodeV1], new_edges: List[EdgeV1], graph: Graph):
        self.new_nodes, self.new_edges = new_nodes, new_edges
        self.graph = graph
        self.analysis = GraphAnalyzer(graph=self.graph)

    @property
    def new_columns(self):
        for node in self.new_nodes:
            node_type = node.spec.metadata.grai.node_type
            if node_type != "Column":
                continue
            yield node

    def type_tests(self) -> Dict[NodeV1, List[TypeTestResult]]:
        errors = False

        result_map = {}
        for node in self.new_columns:
            try:
                original_node = self.graph.get_node(name=node.spec.name, namespace=node.spec.namespace)
            except:
                # This is a new node
                continue

            result = node.spec.metadata.grai.node_attributes.data_type
            affected_nodes = self.analysis.test_type_change(
                namespace=node.spec.namespace, name=node.spec.name, new_type=result
            )
            result_map[node] = [TypeTestResult(node, path) for path in affected_nodes]
        return result_map

    def unique_tests(self) -> Dict[NodeV1, List[UniqueTestResult]]:
        errors = False
        result_map = {}
        for node in self.new_columns:
            try:
                original_node = self.graph.get_node(name=node.spec.name, namespace=node.spec.namespace)
            except:
                # This is a new node
                continue

            result = node.spec.metadata.grai.node_attributes.is_unique
            affected_nodes = self.analysis.test_unique_violations(
                namespace=node.spec.namespace,
                name=node.spec.name,
                expects_unique=result,
            )
            result_map[node] = [UniqueTestResult(node, path) for path in affected_nodes]
        return result_map

    def null_tests(self) -> Dict[NodeV1, List[NullableTestResult]]:
        errors = False
        result_map = {}
        for node in self.new_columns:
            try:
                original_node = self.graph.get_node(name=node.spec.name, namespace=node.spec.namespace)
            except:
                # This is a new node
                continue

            result = node.spec.metadata.grai.node_attributes.is_nullable
            affected_nodes = self.analysis.test_nullable_violations(
                namespace=node.spec.namespace, name=node.spec.name, is_nullable=result
            )
            result_map[node] = [NullableTestResult(node, path) for path in affected_nodes]
        return result_map

    def test_results(self) -> Dict[NodeV1, List[TestResult]]:
        tests = chain(
            self.unique_tests().items(),
            self.null_tests().items(),
            # self.type_tests().items(),
        )

        results: Dict[NodeV1, List[TestResult]] = {}
        for key, values in tests:
            results.setdefault(key, [])
            results[key].extend(values)

        return results
