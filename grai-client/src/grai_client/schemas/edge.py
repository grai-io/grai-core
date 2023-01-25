from typing import Callable, Dict, List, Literal, Optional, Type, Union
from uuid import UUID

from grai_schemas.base import Edge
from grai_schemas.v1.edge import EdgeV1
from pydantic import Field, validator
from typing_extensions import Annotated

EdgeLabels = Literal["edge", "edges", "Edge", "Edges"]
EdgeTypes = Edge
