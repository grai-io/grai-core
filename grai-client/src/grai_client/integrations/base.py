from abc import ABC, abstractmethod
from typing import List, Optional, ParamSpec, Tuple, Union

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceSpec, SourceV1

from grai_client.endpoints.client import BaseClient
from grai_client.update import update


class EventMixin(ABC):
    def __init__(self):
        raise NotImplementedError("The EventMixin is not yet stable or ready for production use.")

    @abstractmethod
    def events(self) -> List[Event]:
        pass

    def update(self):
        super().update()
        update(self.client, self.events())


P = ParamSpec("P")


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

    @classmethod
    def from_client(cls, client: BaseClient, source_name: str, *args: P.args, **kwargs: P.kwargs):
        class WithClient(cls):
            client: BaseClient

            def __init__(self, client: BaseClient, *args: P.args, **kwargs: P.kwargs):
                self.client = client
                super().__init__(*args, **kwargs)

            def update(self):
                update(self.client, self.nodes())
                update(self.client, self.edges())

        source = client.get("Source", name=source_name)
        version = client.id

        return WithClient(client=client, source=source, version=version, *args, **kwargs)


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
