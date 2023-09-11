from abc import ABC, abstractmethod
from typing import List, Tuple

from decouple import config

from workspaces.models import Workspace


class SearchInterface(ABC):
    @abstractmethod
    def search(self, workspace: Workspace, query: str) -> Tuple[List, bool]:
        pass

    def build(self) -> None:
        pass


class SearchClient(SearchInterface):
    @property
    def client(self):
        client = None

        if config("RETAKE_API_URL", None):
            from .retake import RetakeSearch

            client = RetakeSearch()
        else:
            from .basic import BasicSearch

            client = BasicSearch()

        return client

    def search(self, workspace: Workspace, query: str) -> Tuple[List, bool]:
        return self.client.search(workspace, query)

    def build(self):
        return self.client.build()
