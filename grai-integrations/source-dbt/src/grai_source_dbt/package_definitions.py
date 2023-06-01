from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    """ """

    integration_name = "grai-source-dbt"
    metadata_id = "grai_source_dbt"


config = Config()
