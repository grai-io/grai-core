from typing import List, Tuple

from lineage.graph_cache import GraphCache
from workspaces.models import Workspace

from .search import SearchInterface


class BasicSearch(SearchInterface):
    def search(self, workspace: Workspace, query: str) -> Tuple[List, bool]:
        graph = GraphCache(workspace=workspace)

        return (graph.get_tables(search=query), True)
