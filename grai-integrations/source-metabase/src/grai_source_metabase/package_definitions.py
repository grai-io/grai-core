from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    integration_name = "grai-schemas"
    metadata_id = "grai"


config = Config()
