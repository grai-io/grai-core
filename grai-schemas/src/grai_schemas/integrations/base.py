import sys
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.integrations.quarantine import (
    MissingEdgeNodeReason,
    Quarantine,
    QuarantinedEdge,
    QuarantinedEvent,
    QuarantinedNode,
)
from grai_schemas.v1.source import SourceSpec, SourceV1

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

from functools import cache

from pydantic import BaseModel

P = ParamSpec("P")


def verify_edge_ids(
    nodes: List[SourcedNode], edges: List[SourcedEdge]
) -> Tuple[List[SourcedEdge], List[QuarantinedEdge]]:
    node_labels = {(n.spec.namespace, n.spec.name) for n in nodes}

    good_edges = []
    quarantined_edges = []
    for edge in edges:
        source_id = (edge.spec.source.namespace, edge.spec.source.name)
        destination_id = (edge.spec.destination.namespace, edge.spec.destination.name)
        if source_id in node_labels and destination_id in node_labels:
            good_edges.append(edge)
        else:
            reasons = [
                MissingEdgeNodeReason(side=side, node_name=name, node_namespace=namespace)
                for side, (namespace, name) in (("source", source_id), ("destination", destination_id))
                if (namespace, name) not in node_labels
            ]
            quarantined_edges.append(QuarantinedEdge(edge=edge, reasons=reasons))

    # TODO: sentry alerting on quarantine?

    return good_edges, quarantined_edges


class ValidatedResult(BaseModel):
    nodes: List[SourcedNode] = []
    edges: List[SourcedEdge] = []
    events: List[Event] = []


class GraiIntegrationImplementation(ABC):
    source: SourceV1
    version: str

    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
    ):
        self.source = source
        self.version = version if version else "v1"

    @abstractmethod
    def nodes(self) -> List[SourcedNode]:
        pass

    @abstractmethod
    def edges(self) -> List[SourcedEdge]:
        pass

    @abstractmethod
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        pass

    @abstractmethod
    def ready(self) -> bool:
        pass

    def events(self, *args, **kwargs) -> List[Event]:
        return []


class QuarantineAccessor:
    def __init__(self, integration_instance: GraiIntegrationImplementation):
        self._integration = integration_instance
        self._quarantine = Quarantine()

    @property
    def nodes(self) -> List[QuarantinedNode]:
        _ = self._integration.nodes  # Ensure nodes are populated in the quarantine
        return self._quarantine.nodes

    @nodes.setter
    def nodes(self, value: List[QuarantinedNode]):
        self._quarantine.nodes = value

    @property
    def edges(self) -> List[QuarantinedEdge]:
        _ = self._integration.edges  # Ensure edges are populated in the quarantine
        return self._quarantine.edges

    @edges.setter
    def edges(self, value: List[QuarantinedEdge]):
        self._quarantine.edges = value

    @property
    def events(self) -> List[QuarantinedEvent]:
        _ = self._integration.events  # Ensure events are populated in the quarantine
        return self._quarantine.events

    @events.setter
    def events(self, value: List[QuarantinedEvent]):
        self._quarantine.events = value

    @property
    def has_quarantined(self) -> bool:
        return self._quarantine.has_quarantined


class ValidatedIntegration(GraiIntegrationImplementation):
    def __init__(self, integration: GraiIntegrationImplementation, *args, **kwargs):
        self.integration = integration
        self._quarantine_accessor = QuarantineAccessor(self)
        super().__init__(source=self.integration.source, version=self.integration.version)

    @property
    def quarantine(self) -> QuarantineAccessor:
        return self._quarantine_accessor

    @cache
    def nodes(self) -> List[SourcedNode]:
        return self.integration.nodes()

    @cache
    def edges(self) -> List[SourcedEdge]:
        edges, quarantined_edges = verify_edge_ids(*self.integration.get_nodes_and_edges())
        self.quarantine.edges = quarantined_edges
        return edges

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        return self.nodes(), self.edges()

    @cache
    def events(self, *args, **kwargs) -> List[Event]:
        return self.integration.events(*args, **kwargs)

    def ready(self) -> bool:
        return self.integration.ready()
