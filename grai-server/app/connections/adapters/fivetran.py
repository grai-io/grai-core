from .base import BaseAdapter
from grai_schemas.v1.source import SourceV1


class FivetranAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_fivetran.base import FivetranIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )

        def getNumber(value: str | None, default: int = None) -> int | None:
            if value is None or value == "":
                return default

            return int(value)

        def getValue(value: str | None, default: str = None) -> str | None:
            if value is None or value == "":
                return default

            return value

        return FivetranIntegration(
            source=source,
            api_key=metadata.get("api_key"),
            api_secret=secrets.get("api_secret"),
            namespaces=metadata.get("namespaces"),
            default_namespace=self.run.connection.namespace,
            endpoint=getValue(metadata.get("endpoint"), "https://api.fivetran.com/v1"),
            limit=getNumber(metadata.get("limit"), 10000),
            parallelization=getNumber(metadata.get("parallelization"), 10),
        )
