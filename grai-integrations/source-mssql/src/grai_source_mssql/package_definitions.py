from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    integration_name = "grai-source-mssql"
    metadata_id = "grai_source_mssql"


config = Config()
