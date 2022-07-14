from typing import Dict, Type, Callable, Optional, Literal
from typing import List, Optional, Union, Dict
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from grai_cli.settings.schemas.utilities import PlaceHolderSchema


class V1(BaseModel):
    name: str
    namespace: str
    data_source: str
    display_name: Optional[str]
    is_active: Optional[str]
    metadata: Optional[Dict] = {}


class V2(PlaceHolderSchema):
    pass


class NodeV1(BaseModel):
    version: Literal['v1']
    type: Literal['Node']
    spec: V1


class NodeV2(BaseModel):
    version: Literal['v2']
    type: Literal['Node']
    spec: V2


class NodeType:
    pass


Node = Annotated[Union[NodeV1, NodeV2], Field(discriminator='version')]
