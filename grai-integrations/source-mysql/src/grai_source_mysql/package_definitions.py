from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    integration_name = "grai-source-mysql"
    metadata_id = "grai_source_mysql"


config = Config()
