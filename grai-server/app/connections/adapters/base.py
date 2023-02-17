from abc import ABC
from itertools import chain

from grai_graph.graph import build_graph
from grai_schemas.v1 import EdgeV1, NodeV1

from connections.models import Run
from connections.task_helpers import modelToSchema, update
from lineage.models import Edge, Node

from .tools import TestResultCacheBase


class BaseAdapter(ABC):
    run: Run

    def get_nodes_and_edges(self):
        raise NotImplementedError(f"No get_nodes_and_edges implemented for {type(self)}")

    def run_update(self, run: Run):
        self.run = run

        nodes, edges = self.get_nodes_and_edges()

        update(self.run.workspace, nodes)
        update(self.run.workspace, edges)

    def run_tests(self, run: Run):
        self.run = run

        new_nodes, new_edges = self.get_nodes_and_edges()

        nodes = [modelToSchema(model, NodeV1, "Node") for model in Node.objects.filter(workspace=run.workspace)]
        edges = [
            modelToSchema(model, EdgeV1, "Edge")
            for model in Edge.objects.filter(workspace=run.workspace)
            .select_related("source")
            .select_related("destination")
        ]

        graph = build_graph(nodes, edges, "v1")

        results = TestResultCacheBase(new_nodes, new_edges, graph)

        test_failures = list(chain.from_iterable(results.test_results().values()))
        test_list = [test.toJSON() for test in test_failures]

        message = None

        if run.commit and run.trigger:
            message = results.consolidated_summary().message(run)

        return test_list, message
