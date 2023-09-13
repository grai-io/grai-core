import sys
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceSpec, SourceV1

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


class EventMixin(ABC):
    @abstractmethod
    def events(self) -> List[Event]:
        pass

    def update(self):
        super().update()
        update(self.client, self.events())


P = ParamSpec("P")


class QuarantinedEdge:
    edge: SourcedEdge
    source_quarantined: bool
    destination_quarantined: bool

    def __init__(self, edge: SourcedEdge, source_quarantined: bool, destination_quarantined: bool):
        self.edge = edge
        self.source_quarantined = source_quarantined
        self.destination_quarantined = destination_quarantined


def verify_edge_ids(nodes: List[SourcedNode], edges: List[SourcedEdge]):
    node_labels = {(n.spec.namespace, n.spec.name) for n in nodes}

    good_edges = []
    quarantined_edges = []
    for edge in edges:
        source_id = (edge.spec.source.namespace, edge.spec.source.name)
        destination_id = (edge.spec.destination.namespace, edge.spec.destination.name)
        if source_id in node_labels and destination_id in node_labels:
            good_edges.append(edge)
        else:
            quarantined_edge = QuarantinedEdge(edge, source_id not in node_labels, destination_id not in node_labels)
            quarantined_edges.append(quarantined_edge)

    # TODO: sentry alerting on quarantine?

    return good_edges


class GraiIntegrationImplementation(ABC):
    source: SourceV1
    version: str

    def __init__(
        self,
        source: Union[SourceV1, SourceSpec],
        version: Optional[str] = None,
    ):
        self.source = source if isinstance(source, SourceV1) else SourceV1.from_spec(source)
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

    def get_validated_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        nodes, edges = self.get_nodes_and_edges()
        edges = verify_edge_ids(nodes, edges)
        return nodes, edges


class SeparateNodesAndEdgesMixin:
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        return self.nodes(), self.edges()


class CombinedNodesAndEdgesMixin:
    def nodes(self) -> List[SourcedNode]:
        nodes, edges = self.get_nodes_and_edges()
        return nodes

    def edges(self) -> List[SourcedEdge]:
        nodes, edges = self.get_nodes_and_edges()
        return edges


class ConnectorMixin(CombinedNodesAndEdgesMixin):
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        with self.connector.connect() as conn:
            nodes, edges = conn.get_nodes_and_edges()

        nodes = self.adapt_to_client(nodes)
        edges = self.adapt_to_client(edges)
        return nodes, edges

    def ready(self) -> bool:
        with self.connector.connect() as _:
            pass
        return True
