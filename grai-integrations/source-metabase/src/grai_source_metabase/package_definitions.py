from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    integration_name = "grai-source-metabase"
    metadata_id = "grai_source_metabase"


config = Config()
