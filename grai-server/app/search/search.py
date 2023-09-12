from abc import ABC, abstractmethod
from typing import List, Tuple

from decouple import config

from workspaces.models import Workspace


class SearchInterface(ABC):
    @abstractmethod
    def search(self, workspace: Workspace, query: str) -> Tuple[List, bool]:
        pass  # pragma: no cover

    def build(self) -> None:
        pass


class SearchClient(SearchInterface):
    @property
    def client(self):
        if config("RETAKE_API_URL", None):
            from .retake import RetakeSearch

            return RetakeSearch()

        from .basic import BasicSearch

        return BasicSearch()

    def search(self, workspace: Workspace, query: str) -> Tuple[List, bool]:
        return self.client.search(workspace, query)

    def build(self):
        return self.client.build()
