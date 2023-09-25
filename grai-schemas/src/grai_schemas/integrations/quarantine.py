from abc import ABC, abstractmethod
from typing import List, Literal, Set

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from pydantic import BaseModel


class QuarantineReason(BaseModel, ABC):
    """Base class for quarantine reasons"""

    @property
    @abstractmethod
    def reason(self) -> str:
        """Returns a string describing the reason for quarantine"""
        pass


class MissingEdgeNodeReason(QuarantineReason):
    """Class definition of MissingEdgeNodeReason

    Attributes:
        side: Either Source or Destination
        node_name: The name of the missing node
        node_namespace: The namespace of the missing node

    """

    side: Literal["source", "destination"]
    node_name: str
    node_namespace: str

    @property
    def reason(self) -> str:
        """Returns a string describing the reason for quarantine"""
        return f"{self.side.capitalize()} node `({self.node_name}, {self.node_namespace})` was not found."


class QuarantinedEdge(BaseModel):
    """Class definition of QuarantinedEdge

    Attributes:
        edge: The edge that was quarantined
        reasons: A list of reasons for quarantine

    """

    edge: SourcedEdge
    reasons: List[QuarantineReason]


class QuarantinedNode(BaseModel):
    """Class definition of QuarantinedNode

    Attributes:
        node: The node that was quarantined
        reasons: A list of reasons for quarantine

    """

    node: SourcedNode
    reasons: List[QuarantineReason]


class QuarantinedEvent(BaseModel):
    """Class definition of QuarantinedEvent

    Attributes:
        event: The event that was quarantined
        reasons: A list of reasons for quarantine

    """

    event: Event
    reasons: List[QuarantineReason]


class Quarantine(BaseModel):
    """Class definition of Quarantine

    Attributes:
        nodes: A list of quarantined nodes
        edges: A list of quarantined edges
        events: A list of quarantined events

    """

    nodes: List[QuarantinedNode] = []
    edges: List[QuarantinedEdge] = []
    events: List[QuarantinedEvent] = []

    @property
    def has_quarantined(self):
        """Returns True if there are any quarantined objects in the Quarantine"""
        return self.nodes or self.edges or self.events
