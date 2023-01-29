from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, root_validator

from grai_source_dbt.models.shared import DBTNode


class TestConfig(BaseModel):
    enabled: bool
    alias: Optional[str]
    test_schema: str = Field(alias="schema")
    database: Optional[str]
    tags: Union[str, List[str]]
    meta: Dict
    materialized: Literal["test"]
    severity: Union[Literal["ERROR"], Literal["error"], Literal["WARN"], Literal["warn"]]
    store_failures: Optional[bool]
    where: Optional[str]
    limit: Optional[int]
    fail_calc: str
    warn_if: str
    error_if: str

    @property
    def tag_list(self) -> List[str]:
        return [self.tags] if isinstance(self.tags, str) else self.tags


# TODO: Multiple different types of tests with distinct metadata keyword options
class TestMetadata(BaseModel):
    name: str
    namespace: Optional[str]
    kwargs: Dict[str, Any]


class Test(DBTNode):
    raw_sql: str
    test_metadata: TestMetadata
    config: TestConfig
    column_name: Optional[str]
    file_key_name: str
    test_schema: str = Field(alias="schema")
    resource_type: Literal["test"]

    @property
    def full_name(self):
        return f"{self.unique_id}"
