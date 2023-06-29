from abc import ABC, abstractmethod
from typing import Generic, List, Tuple, TypeVar

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceSpec, SourceV1

from grai_client.endpoints.v1.client import ClientV1
from grai_client.update import update


class EventMixin(ABC):
    def __init__(self):
        raise NotImplementedError("The EventMixin is not yet stable or ready for production use.")

    @abstractmethod
    def events(self) -> List[Event]:
        pass

    def update(self):
        update(self.client, self.events())
        super().update()


T = TypeVar("T")


class GraiIntegrationImplementationV1(Generic[T], ABC):
    client: ClientV1
    source: SourceV1
    params: T

    @classmethod
    def from_client(cls, client: ClientV1, source_name: str, params: T):
        if client.id != "v1":
            raise NotImplementedError(f"No available implementation for client version {client.id}")

        instance = cls()

        instance.client = client
        instance.params = params
        instance.source = client.get("Source", name=source_name)
        instance.setup(params)

        return instance

    @classmethod
    def from_source(cls, source: SourceSpec, params: T):
        instance = cls()

        instance.params = params
        instance.source = SourceV1.from_spec(source)
        instance.setup(params)

        return instance

    def setup(self):
        pass

    @abstractmethod
    def nodes(self) -> List[SourcedNode]:
        pass

    @abstractmethod
    def edges(self) -> List[SourcedEdge]:
        pass

    @abstractmethod
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        pass

    def update(self):
        if not self.client:
            raise Exception("Cannot update without a client")

        update(self.client, self.nodes())
        update(self.client, self.edges())


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

        nodes = self.adapt_to_client(nodes, self.source, self.client.id)
        edges = self.adapt_to_client(edges, self.source, self.client.id)
        return nodes, edges
