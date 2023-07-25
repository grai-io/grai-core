from abc import ABC
from itertools import chain
from typing import Optional

from django.db.models import Max
from grai_graph.graph import build_graph
from grai_schemas.v1 import EdgeV1, NodeV1

from connections.models import Run
from connections.task_helpers import modelToSchema, update
from lineage.models import Edge, Event, Node

from .tools import TestResultCacheBase


class BaseAdapter(ABC):
    run: Run

    def get_integration(self):
        raise NotImplementedError(f"No get_integration implemented for {type(self)}")

    def get_nodes_and_edges(self):
        return self.get_integration().get_nodes_and_edges()

    def events(self, last_event_date):
        return self.get_integration().events(last_event_date)

    def run_validate(self, run: Run) -> bool:
        self.run = run

        return self.get_integration().ready()

    def run_update(self, run: Run):
        self.run = run

        nodes, edges = self.get_nodes_and_edges()

        update(self.run.workspace, self.run.source, nodes)
        update(self.run.workspace, self.run.source, edges)

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

    def run_events(self, run: Run, all: bool = False):
        self.run = run

        last_event_date = None

        if not all:
            last_event_date = Event.objects.filter(connection=run.connection).aggregate(Max("date"))["date__max"]

        events = self.events(last_event_date)

        connection = run.connection

        existing_event_references = connection.events.values_list("reference", flat=True)

        for event in events:
            if str(event.reference) not in existing_event_references:
                event_model = connection.events.create(
                    workspace=run.workspace,
                    reference=event.reference,
                    date=event.date,
                    status=event.status,
                    metadata=event.metadata,
                )

                if event.nodes:
                    nodes = Node.objects.filter(
                        workspace=run.workspace,
                        namespace=run.connection.namespace,
                        name__in=event.nodes,
                    )

                    if len(nodes) != len(event.nodes):
                        print("Some nodes not found")

                    event_model.nodes.add(*nodes)
