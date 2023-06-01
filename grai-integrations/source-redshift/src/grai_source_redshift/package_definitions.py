from grai_schemas.generics import PackageConfig


class Config(PackageConfig):
    """ """

    integration_name = "grai-source-redshift"
    metadata_id = "grai_source_redshift"


config = Config()
