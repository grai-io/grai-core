from abc import ABC, abstractmethod
from itertools import chain, pairwise
from typing import Dict, Iterable, List, Tuple

from decouple import config
from grai_graph.analysis import Graph, GraphAnalyzer
from grai_schemas.v1 import EdgeV1, NodeV1

from connections.models import Run

SEPARATOR_CHAR = "/"


def build_node_name(node: NodeV1) -> str:
    return f"{node.spec.namespace}{SEPARATOR_CHAR}{node.spec.name}"


def collapsable(content, label):
    result = f"""<details><summary>{label}</summary>
<p>

{content}

</p>
</details>"""
    return result


def heading(string, level):
    return f"<h{level}> {string} </h{level}>"


class TestResult(ABC):
    """Assumed to be a failing test result"""

    type: str

    def __init__(self, node: NodeV1, test_path: List[NodeV1], test_pass: bool = False):
        self.node = node
        self.failing_node = test_path[-1]
        self.test_path = test_path
        self.node_name = build_node_name(self.node)
        self.failing_node_name = build_node_name(self.failing_node)
        self.test_pass = test_pass

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
            "message": self.message(),
            "test_pass": self.test_pass,
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


class TestSummary:
    def __init__(self, test_results):
        self.test_results: List[TestResult] = test_results

    def graph_status_path(self) -> Dict[Tuple[str, str], Dict[Tuple[str, str], bool]]:
        edge_status: Dict[Tuple[str, str], Dict[Tuple[str, str], bool]] = {}
        for test in self.test_results:
            path_edges = list(pairwise(test.test_path))
            if len(path_edges) < 1:
                raise Exception("Test paths must have more than two nodes")

            for a, b in path_edges:
                a_id = (a.spec.namespace, a.spec.name)
                b_id = (b.spec.namespace, b.spec.name)
                edge_status.setdefault(a_id, {})
                edge_status[a_id].setdefault(b_id, True)
            edge_status[a_id][b_id] = False

        return edge_status

    def mermaid_graph(self) -> str:
        def new_edge(a, b, status):
            a, b = [f"{namespace}{SEPARATOR_CHAR}{name}" for namespace, name in [a, b]]
            return f'\t{a}-->|"{"✅" if status else "❌"}"| {b};'

        graph_status = self.graph_status_path()
        edges = "\n".join(new_edge(a, b, status) for a, values in graph_status.items() for b, status in values.items())
        message = f"```mermaid\ngraph TD;\n{edges}\n```"
        return message

    def build_table(self) -> str:
        rows = "\n".join([test.make_row() for test in self.test_results])
        message = f"| Namespace | Changed Node | Failing Dependency | Test | Message |\n| --- | --- | --- | --- | --- |\n{rows}"
        return message

    def test_summary(self) -> str:
        label = heading("Test Results", 2)
        section = f"\n{self.build_table()}\n"
        return collapsable(section, label)

    def build_link(self, run: Run, frontend_url: str):
        link_start = f"{frontend_url}/{run.workspace.organisation.name}/{run.workspace.name}/reports/github/{run.commit.repository.owner}/{run.commit.repository.repo}"
        link = f"{link_start}/pulls/{run.commit.pull_request.reference}"

        return link, f"""<a href="{link}" target="_blank">View full report at Grai.</a>"""

    def message(self, run: Run) -> str:
        message = f"\n{self.mermaid_graph()}\n\n{self.test_summary()}\n"

        frontend_url = config("FRONTEND_URL", "http://localhost:3000")

        if frontend_url and run.commit.pull_request is not None:
            message = f"{message}\n{self.build_link(run, frontend_url)[1]}"

        return message


class SingleSourceTestSummary(TestSummary):
    def __init__(self, source_node, test_results, *args, **kwargs):
        self.source_node = source_node
        super().__init__(test_results, *args, **kwargs)

    def test_summary(self) -> str:
        label = heading(build_node_name(self.source_node), 2)
        section = f"{heading('Failing Tests', 4)}\n\n{self.build_table()}\n"
        return collapsable(section, label)


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

    def data_type_tests(self) -> Dict[NodeV1, List[TypeTestResult]]:
        result_map = {}

        for node in self.new_columns:
            result = node.spec.metadata.grai.node_attributes.data_type
            affected_nodes = self.analysis.test_data_type_change(
                namespace=node.spec.namespace, name=node.spec.name, new_type=result
            )
            result_map[node] = [TypeTestResult(node, path, test_pass) for (path, test_pass) in affected_nodes]

        return result_map

    def unique_tests(self) -> Dict[NodeV1, List[UniqueTestResult]]:
        result_map = {}

        for node in self.new_columns:
            result = node.spec.metadata.grai.node_attributes.is_unique
            affected_nodes = self.analysis.test_unique_violations(
                namespace=node.spec.namespace,
                name=node.spec.name,
                expects_unique=result,
            )
            result_map[node] = [UniqueTestResult(node, path, test_pass) for (path, test_pass) in affected_nodes]

        return result_map

    def null_tests(self) -> Dict[NodeV1, List[NullableTestResult]]:
        result_map = {}

        for node in self.new_columns:
            result = node.spec.metadata.grai.node_attributes.is_nullable
            affected_nodes = self.analysis.test_nullable_violations(
                namespace=node.spec.namespace, name=node.spec.name, is_nullable=result
            )
            result_map[node] = [NullableTestResult(node, path, test_pass) for (path, test_pass) in affected_nodes]

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

    def test_failures(self) -> Dict[NodeV1, List[TestResult]]:
        tests = chain(
            self.unique_tests().items(),
            self.null_tests().items(),
            # self.type_tests().items(),
        )

        results: Dict[NodeV1, List[TestResult]] = {}
        for key, values in tests:
            failures = list(filter(lambda x: not x.test_pass, values))
            if len(failures) > 0:
                results.setdefault(key, [])
                results[key].extend(values)

        return results

    def messages(self) -> Iterable[str]:
        test_results = self.test_results()
        for node, tests in test_results.items():
            yield SingleSourceTestSummary(node, tests).message()

    def consolidated_summary(self) -> TestSummary:
        test_failures = list(chain.from_iterable(self.test_failures().values()))
        summary = TestSummary(test_failures)
        return summary
