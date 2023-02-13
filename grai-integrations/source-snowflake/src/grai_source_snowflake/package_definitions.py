from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    integration_name = "grai-source-snowflake"
    metadata_id = "grai_source_snowflake"


config = Config()
