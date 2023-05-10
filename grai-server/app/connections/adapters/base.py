from abc import ABC
from itertools import chain

from grai_graph.graph import build_graph
from grai_schemas.v1 import EdgeV1, NodeV1

from connections.models import Run
from connections.task_helpers import modelToSchema, update
from lineage.models import Edge, Event, Node

from .tools import TestResultCacheBase


class BaseAdapter(ABC):
    run: Run

    def get_nodes_and_edges(self):
        raise NotImplementedError(f"No get_nodes_and_edges implemented for {type(self)}")

    def get_events(self):
        raise NotImplementedError(f"No get_events implemented for {type(self)}")

    def run_validate(self, run: Run):
        self.run = run

        self.get_nodes_and_edges()

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

        test_results = list(chain.from_iterable(results.test_results().values()))
        test_list = [test.toJSON() for test in test_results]

        message = None

        if run.commit and run.trigger:
            message = results.consolidated_summary().message(run)

        return test_list, message

    def run_events(self, run: Run):
        self.run = run

        events = self.get_events()

        connection = run.connection

        existing_event_ids = connection.events.values_list("metadata__grai_source_dbt_cloud__id", flat=True)

        for event in events:
            if event["id"] not in existing_event_ids:
                connection.events.create(
                    workspace=run.workspace,
                    date=event["created_at"],
                    status=Event.SUCCESS if event["status"] == 10 else Event.ERROR,
                    metadata={
                        "grai_source_dbt_cloud": event,
                    },
                )
