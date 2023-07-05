from abc import ABC, abstractmethod
from typing import List, Optional, ParamSpec, Tuple, Union

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceSpec, SourceV1

from grai_client.endpoints.client import BaseClient
from grai_client.update import update


class EventMixin(ABC):
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
        def get_source(source_name: str) -> SourceV1:
            sources = client.get("Source", name=source_name)
            assert len(sources) == 1, f"Expected 1 source, got {len(sources)}"
            return sources[0]

        class WithClient(cls):
            client: BaseClient

            def __init__(
                self,
                client: BaseClient,
                source: SourceV1,
                version: str,
                *args: P.args,
                **kwargs: P.kwargs,
            ):
                self.client = client
                super().__init__(source=source, version=version, *args, **kwargs)

            def update(self):
                update(self.client, self.nodes())
                update(self.client, self.edges())

        if (kwargs_version := kwargs.pop("version", None)) is not None:
            if kwargs_version != client.id:
                raise Exception(
                    f"Client version mismatch, the user provided version=`{kwargs_version}` does not match the "
                    f"client id=`{client.id}`. Either leave `version` empty or set it to the client id."
                )
        version = client.id
        source = get_source(source_name)

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
