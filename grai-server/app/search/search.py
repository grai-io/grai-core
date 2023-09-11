from retakesearch import Client, Database, Table
from decouple import config

client = Client(
    api_key=config("RETAKE_API_KEY", "retake-test-key"),
    url=config("RETAKE_API_URL", "http://localhost:8002"),
)

database = Database(
    dbname=config("DB_NAME", default="grai"),
    host=config("DB_HOST", default="db"),
    port=int(config("DB_PORT", default="5432")),
    user=config("DB_USER", default="grai"),
    password=config("DB_PASSWORD", default="grai"),
)


class Search:
    index_name = "nodes"
    columns = [
        "id",
        "name",
        "namespace",
        "display_name",
        "workspace_id",
        "metadata->grai->node_type",
    ]

    def __init__(self):
        self.table = Table(
            name="lineage_node",
            columns=self.columns,
            transform={
                "mapping": {"workspace_id": "keyword"},
                "rename": {
                    "metadata_grai_node_type": "node_type",
                },
            },
        )

    def create(self):
        try:
            index = client.get_index(index_name=self.index_name)
        except:
            index = client.create_index(index_name=self.index_name)

        if not index:
            raise ValueError("Table failed to index due to an unexpected error")

        index.vectorize(self.columns)
        index.add_source(database=database, table=self.table)
