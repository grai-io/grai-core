from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, Field


class AccountsMetadataResponse(BaseModel):
    id: Optional[str] = Field(None, description="The unique account identifier")
    name: Optional[str] = Field(None, description="The account name")


class RunsMetadataResponse(BaseModel):
    id: Optional[str] = Field(None, description="The unique account identifier")
