from abc import ABC, abstractmethod
from typing import List, Optional

from decouple import config

from workspaces.models import Workspace


class SearchInterface(ABC):
    @abstractmethod
    def search(self, workspace: Workspace, query: str) -> List:
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

    def search(self, workspace: Workspace, query: Optional[str]) -> List:
        return self.client.search(workspace, query)

    def build(self):
        return self.client.build()
