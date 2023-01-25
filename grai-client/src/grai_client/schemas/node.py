from typing import Dict, Literal

from grai_schemas.base import Node
from grai_schemas.generics import GraiBaseModel
from grai_schemas.v1.node import NodeIdTypes, NodeV1

NodeLabels = Literal["node", "nodes", "Node", "Nodes"]
NodeTypes = Node
