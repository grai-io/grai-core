from typing import List, Tuple

from decouple import config
from retakesearch import Client, Database, Search, Table

from workspaces.models import Workspace

from .search import SearchInterface

client = Client(
    api_key=config("RETAKE_API_KEY"),
    url=config("RETAKE_API_URL"),
)


class RetakeSearch(SearchInterface):
    index_name = "nodes"
    columns = [
        "id",
        "name",
        "namespace",
        "display_name",
        "workspace_id",
        "metadata->grai->node_type",
    ]

    def build(self):
        database = Database(
            dbname=config("DB_NAME", default="grai"),
            host=config("DB_HOST", default="db"),
            port=int(config("DB_PORT", default="5432")),
            user=config("DB_USER", default="grai"),
            password=config("DB_PASSWORD", default="grai"),
        )

        table = Table(
            name="lineage_node",
            columns=self.columns,
            transform={
                "mapping": {"workspace_id": "keyword"},
                "rename": {
                    "metadata_grai_node_type": "node_type",
                },
            },
        )

        try:
            index = client.get_index(index_name=self.index_name)
        except:
            index = client.create_index(index_name=self.index_name)

        if not index:
            raise ValueError("Table failed to index due to an unexpected error")

        index.vectorize(self.columns)
        index.add_source(database=database, table=table)

    def search(self, workspace: Workspace, query: str) -> Tuple[List, bool]:
        index = client.get_index(self.index_name)

        dsl = {"query": {"query_string": {"query": f"workspace_id.keyword:{str(workspace.id)}"}}}
        bm25_search_query = (
            Search()
            .from_dict(dsl)
            # .query("fuzzy", display_name={"value": query, "fuzziness": 10})
            .filter("term", node_type="table")
            .with_neural(query=query, fields=["display_name"])
        )

        result = index.search(bm25_search_query)

        hits = result.get("hits", {"hits": []}).get("hits", [])

        return ([hit["_source"] for hit in hits], False)
