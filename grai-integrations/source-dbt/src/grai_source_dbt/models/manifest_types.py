from typing import Annotated, Union

from grai_source_dbt.models.nodes import Model, Seed, Source
from grai_source_dbt.models.tests import Test
from pydantic import BaseModel, Field

# class ManifestNode(BaseModel):
#     __root__: Annotated[Union[Model, Seed, Test], Field(discriminator='resource_type')]

ManifestNode = Annotated[Union[Model, Seed, Test], Field(discriminator="resource_type")]
