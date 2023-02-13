from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    integration_name = "grai-source-bigquery"
    metadata_id = "grai_source_bigquery"


config = Config()
