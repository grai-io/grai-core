from abc import ABC, abstractmethod
from typing import List, Literal, Set

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from pydantic import BaseModel


class QuarantineReason(BaseModel, ABC):
    @property
    @abstractmethod
    def reason(self) -> str:
        pass


class MissingEdgeNodeReason(QuarantineReason):
    side: Literal["source", "destination"]
    node_name: str
    node_namespace: str

    @property
    def reason(self) -> str:
        return f"{self.side.capitalize()} node `({self.node_name}, {self.node_namespace})` was not found."


class QuarantinedEdge(BaseModel):
    edge: SourcedEdge
    reasons: List[QuarantineReason]


class QuarantinedNode(BaseModel):
    node: SourcedNode
    reasons: List[QuarantineReason]


class QuarantinedEvent(BaseModel):
    event: Event
    reasons: List[QuarantineReason]


class Quarantine(BaseModel):
    nodes: List[QuarantinedNode] = []
    edges: List[QuarantinedEdge] = []
    events: List[QuarantinedEvent] = []

    @property
    def has_quarantined(self):
        return self.nodes or self.edges or self.events
