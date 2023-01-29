from typing import Annotated, Union

from pydantic import BaseModel, Field

from grai_source_dbt.models.nodes import Model, Seed, Snapshot, Source
from grai_source_dbt.models.tests import Test

# class ManifestNode(BaseModel):
#     __root__: Annotated[Union[Model, Seed, Test], Field(discriminator='resource_type')]

ManifestNode = Annotated[Union[Model, Seed, Snapshot, Test], Field(discriminator="resource_type")]
