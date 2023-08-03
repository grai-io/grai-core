from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


class LookerNode(BaseModel):
    """ """

    pass


class Dashboard(LookerNode):
    """ """

    name: str = Field(alias="id")
    display_name: str = Field(alias="title")
