from grai_schemas.models import GraiNodeMetadata
from pydantic import BaseModel


class Metadata(BaseModel):
    grai: GraiNodeMetadata
