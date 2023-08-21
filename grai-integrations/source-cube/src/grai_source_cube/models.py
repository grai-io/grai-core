from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel

"""
This module contains structured pydantic objects representing cube.js concepts or API responses which would be used
by the loader to create raw edges and nodes for the graph. We will eventually transform these into grai_schemas
objects in the adapter module.
"""


NodeTypes = Union[Question, Table, Collection, Column]  # these will be specific implementations for Cube


class Edge(BaseModel):
    source: NodeTypes
    destination: NodeTypes
    definition: Optional[str]
    metadata: Optional[Dict] = None
    namespace: str
