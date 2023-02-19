from .base import BaseAdapter


class FivetranAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_fivetran.base import get_nodes_and_edges
        from grai_source_fivetran.loader import FivetranConnector

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        def getNumber(value: str | None, default: int = None) -> int | None:
            if value is None or value == "":
                return default

            return int(value)

        def getValue(value: str | None, default: str = None) -> str | None:
            if value is None or value == "":
                return default

            return value

        conn = FivetranConnector(
            api_key=metadata.get("api_key"),
            api_secret=secrets.get("api_secret"),
            namespaces=metadata.get("namespaces"),
            default_namespace=self.run.connection.namespace,
            endpoint=getValue(metadata.get("endpoint"), "https://api.fivetran.com/v1"),
            limit=getNumber(metadata.get("limit"), 10000),
            parallelization=getNumber(metadata.get("parallelization"), 10),
        )

        return get_nodes_and_edges(conn, "v1")
