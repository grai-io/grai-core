from abc import ABC, abstractmethod
from functools import cached_property
from itertools import chain
from typing import List, Tuple

import sentry_sdk
from django.db.models import Max
from grai_graph.graph import build_graph
from grai_schemas.integrations.base import ValidatedIntegration
from grai_schemas.v1 import EdgeV1, NodeV1

from connections.models import Run
from connections.task_helpers import modelToSchema, update
from lineage.models import Edge, Event, Node

from .tools import TestResultCacheBase


class QuarantinedItemException(Exception):
    pass


def capture_quarantined_errors(integration: ValidatedIntegration, run: Run):
    with sentry_sdk.push_scope() as scope:
        scope.set_extra("integration", integration.integration.__class__.__name__)
        scope.set_extra("workspace", run.workspace.name)
        scope.set_extra("organization", run.workspace.organisation)
        scope.set_extra("source", run.source.name)
        scope.set_tag("error_type", "QuarantinedItems")

        if integration.quarantine.nodes:
            error_types = {type(reason) for item in integration.quarantine.nodes for reason in item}
            error = QuarantinedItemException(f"Quarantined node with {error_types}")
            sentry_sdk.capture_exception(error)

        if integration.quarantine.edges:
            error_types = {type(reason) for item in integration.quarantine.edges for reason in item}
            error = QuarantinedItemException(f"Quarantined edge with {error_types}")
            sentry_sdk.capture_exception(error)

        if integration.quarantine.events:
            error_types = {type(reason) for item in integration.quarantine.events for reason in item}
            error = QuarantinedItemException(f"Quarantined event with {error_types}")
            sentry_sdk.capture_exception(error)


class BaseAdapter(ABC):
    def __init__(self, run: Run):
        self.run = run

    @abstractmethod
    def run_validate(self) -> bool:
        pass

    @abstractmethod
    def get_nodes_and_edges(self):
        pass

    @abstractmethod
    def run_update(self):
        pass

    def run_tests(self) -> Tuple[List, str]:
        new_nodes, new_edges = self.get_nodes_and_edges()

        nodes = [modelToSchema(model, NodeV1, "Node") for model in Node.objects.filter(workspace=self.run.workspace)]
        edges = [
            modelToSchema(model, EdgeV1, "Edge")
            for model in Edge.objects.filter(workspace=self.run.workspace)
            .select_related("source")
            .select_related("destination")
        ]

        graph = build_graph(nodes, edges, "v1")

        results = TestResultCacheBase(new_nodes, new_edges, graph)

        test_results = list(chain.from_iterable(results.test_results().values()))
        test_list = [test.toJSON() for test in test_results]

        message = None

        if self.run.commit and self.run.trigger:
            message = results.consolidated_summary().message(self.run)

        return test_list, message

    def run_events(self, run_all: bool = False):
        last_event_date = None

        if not run_all:
            last_event_date = Event.objects.filter(connection=self.run.connection).aggregate(Max("date"))["date__max"]

        events = self.events(last_event_date)

        existing_event_references = self.run.connection.events.values_list("reference", flat=True)

        for event in events:
            if str(event.reference) not in existing_event_references:
                event_model = self.run.connection.events.create(
                    workspace=self.run.workspace,
                    reference=event.reference,
                    date=event.date,
                    status=event.status,
                    metadata=event.metadata,
                )

                if event.nodes:
                    nodes = Node.objects.filter(
                        workspace=self.run.workspace,
                        namespace=self.run.connection.namespace,
                        name__in=event.nodes,
                    )

                    if len(nodes) != len(event.nodes):
                        print("Some nodes not found")

                    event_model.nodes.add(*nodes)


class IntegrationAdapter(BaseAdapter):
    @abstractmethod
    def get_integration(self):
        raise NotImplementedError(f"No get_integration implemented for {type(self)}")

    @cached_property
    def integration(self) -> ValidatedIntegration:
        return ValidatedIntegration(self.get_integration())

    def get_nodes_and_edges(self):
        return self.integration.get_nodes_and_edges()

    def run_update(self):
        nodes, edges = self.integration.get_nodes_and_edges()
        capture_quarantined_errors(self.integration, self.run)
        update(self.run.workspace, self.run.source, nodes)
        update(self.run.workspace, self.run.source, edges)

    def events(self, last_event_date):
        events = self.integration.events(last_event_date)
        capture_quarantined_errors(self.integration, self.run)

        return events

    def run_validate(self) -> bool:
        return self.integration.ready()
