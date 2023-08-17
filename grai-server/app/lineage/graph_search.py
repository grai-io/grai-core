from retakesearch import Client, Search
from workspaces.models import Workspace


class GraphSearch:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.client = Client(api_key="retake-test-key", url="http://localhost:8002")

    def search(self, query):
        index_name = "nodes"

        index = self.client.get_index(index_name)

        dsl = {"query": {"query_string": {"query": f"workspace_id.keyword:{str(self.workspace.id)}"}}}
        bm25_search_query = (
            Search()
            .from_dict(dsl)
            # .query("fuzzy", display_name={"value": query, "fuzziness": 10})
            .filter("term", node_type="table")
            .with_neural(query=query, fields=["display_name"])
        )

        result = index.search(bm25_search_query)

        hits = result.get("hits", {"hits": []}).get("hits", [])
        return [hit["_source"] for hit in hits]
