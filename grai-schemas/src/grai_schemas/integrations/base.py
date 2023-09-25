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
    """Validates that all edges have a source and destination node in the graph

    Args:
        nodes: A list of sourced nodes
        edges: A list of sourced edges

    Returns:
        A tuple of lists of sourced edges. The first list contains all edges that have a source and destination node in the graph. The second list contains all edges that do not have a source or destination node in the graph.

    """
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
    """Class definition of ValidatedResult

    Attributes:
        nodes: A list of sourced nodes
        edges: A list of sourced edges
        events: A list of events

    """

    nodes: List[SourcedNode] = []
    edges: List[SourcedEdge] = []
    events: List[Event] = []


class GraiIntegrationImplementation(ABC):
    """Base class for Grai integrations

    Attributes:
        source: The Grai data source to associate with output from the integration.
        version: The Grai data version to associate with output from the integration.

    """

    source: SourceV1
    version: str

    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
    ):
        """Initializes the Grai integration.

        Args:
            source: The Grai data source to associate with output from the integration.
            version: The Grai data version to associate with output from the integration.

        """
        self.source = source
        self.version = version if version else "v1"

    @abstractmethod
    def nodes(self) -> List[SourcedNode]:
        """Returns a list of sourced nodes"""
        pass

    @abstractmethod
    def edges(self) -> List[SourcedEdge]:
        """Returns a list of sourced edges"""
        pass

    @abstractmethod
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of sourced nodes and sourced edges"""
        pass

    @abstractmethod
    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        pass

    def events(self, *args, **kwargs) -> List[Event]:
        """Returns a list of events"""
        return []


class QuarantineAccessor:
    """Class definition of QuarantineAccessor

    Attributes:
        nodes: A list of quarantined nodes
        edges: A list of quarantined edges
        events: A list of quarantined events
        has_quarantined: True if there are any quarantined items.

    """

    def __init__(self, integration_instance: GraiIntegrationImplementation):
        """Initializes the QuarantineAccessor"""
        self._integration = integration_instance
        self._quarantine = Quarantine()

    @property
    def nodes(self) -> List[QuarantinedNode]:
        """Returns a list of quarantined nodes"""
        _ = self._integration.nodes  # Ensure nodes are populated in the quarantine
        return self._quarantine.nodes

    @nodes.setter
    def nodes(self, value: List[QuarantinedNode]):
        """Sets the list of quarantined nodes"""
        self._quarantine.nodes = value

    @property
    def edges(self) -> List[QuarantinedEdge]:
        """Returns a list of quarantined edges"""
        _ = self._integration.edges  # Ensure edges are populated in the quarantine
        return self._quarantine.edges

    @edges.setter
    def edges(self, value: List[QuarantinedEdge]):
        """Sets the list of quarantined edges"""
        self._quarantine.edges = value

    @property
    def events(self) -> List[QuarantinedEvent]:
        """Returns a list of quarantined events"""
        _ = self._integration.events  # Ensure events are populated in the quarantine
        return self._quarantine.events

    @events.setter
    def events(self, value: List[QuarantinedEvent]):
        """Sets the list of quarantined events"""
        self._quarantine.events = value

    @property
    def has_quarantined(self) -> bool:
        """Returns True if there are any quarantined items"""
        return self._quarantine.has_quarantined


class ValidatedIntegration(GraiIntegrationImplementation):
    """A type of Integration which quarantines invalid integration output

    Attributes:
        integration: The integration to validate

    """

    def __init__(self, integration: GraiIntegrationImplementation, *args, **kwargs):
        """Initializes the ValidatedIntegration

        Args:
            integration: The integration to validate

        """
        self.integration = integration
        self._quarantine_accessor = QuarantineAccessor(self)
        super().__init__(source=self.integration.source, version=self.integration.version)

    @property
    def quarantine(self) -> QuarantineAccessor:
        """Returns the QuarantineAccessor for the integration"""
        return self._quarantine_accessor

    @cache
    def nodes(self) -> List[SourcedNode]:
        """Returns a list of validated sourced nodes"""
        return self.integration.nodes()

    @cache
    def edges(self) -> List[SourcedEdge]:
        """Returns a list of validates sourced edges"""
        edges, quarantined_edges = verify_edge_ids(*self.integration.get_nodes_and_edges())
        self.quarantine.edges = quarantined_edges
        return edges

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of validated sourced nodes and sourced edges"""
        return self.nodes(), self.edges()

    @cache
    def events(self, *args, **kwargs) -> List[Event]:
        """Returns a list of validated events"""
        return self.integration.events(*args, **kwargs)

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        return self.integration.ready()
