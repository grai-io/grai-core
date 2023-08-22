import sys
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceSpec, SourceV1

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


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

    @abstractmethod
    def ready(self) -> bool:
        pass


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
