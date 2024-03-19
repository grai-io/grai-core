from grai_schemas.v1.source import SourceV1
from grai_source_cube.base import CubeIntegration
from grai_source_cube.settings import CubeApiConfig
from .base import IntegrationAdapter


def get_config(metadata) -> CubeApiConfig:
    return CubeApiConfig(
        api_token=metadata.get("api_token"),
        api_url=metadata.get("api_url"),
    )


def get_value(value: str | None, default: str | None = None) -> str | None:
    if value is None or value == "":
        return default

    return value


class CubeAdapter(IntegrationAdapter):
    def get_integration(self) -> CubeIntegration:
        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        config = CubeApiConfig(
            api_token=secrets.get("api_token"),
            api_url=metadata.get("api_url"),
        )

        integration = CubeIntegration(
            source=source,
            config=config,
            namespace=self.run.connection.namespace,
            namespace_map=metadata.get("namespace_map"),
        )
        return integration
