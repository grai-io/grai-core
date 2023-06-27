from abc import ABC, abstractmethod
from typing import List, Tuple

from grai_schemas.base import Event, Source, SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceV1

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


class GraiIntegrationImplementationV1(ABC):
    client: ClientV1
    source: SourceV1

    def __init__(self, client: ClientV1, source_name: str):
        self.client = client
        self.source = client.get("Source", name=source_name)

    @abstractmethod
    def nodes(self) -> List[SourcedNode]:
        pass

    @abstractmethod
    def edges(self) -> List[SourcedEdge]:
        pass

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        return self.nodes(), self.edges()

    def update(self):
        update(self.client, self.nodes())
        update(self.client, self.nodes())
