from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    integration_name = "grai-source-postgres"
    metadata_id = "grai_source_postgres"


config = Config()
