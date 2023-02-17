from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    integration_name = "grai-source-fivetran"
    metadata_id = "grai_source_fivetran"


config = Config()
