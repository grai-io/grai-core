from typing import List, Optional

from lineage.graph_cache import GraphCache
from workspaces.models import Workspace

from .search import SearchInterface


class BasicSearch(SearchInterface):
    def search(self, workspace: Workspace, query: Optional[str]) -> List:
        graph = GraphCache(workspace=workspace)

        return graph.get_tables(search=query)
