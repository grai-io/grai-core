from typing import List, Optional

import strawberry


@strawberry.type
class GraphTable:
    id: str
    name: str
    display_name: str
    namespace: str
    data_source: Optional[str]
    x: int
    y: int
    columns: List["GraphColumn"]
    sources: List[str]
    destinations: List[str]
    table_destinations: Optional[List[str]]
    table_sources: Optional[List[str]]


@strawberry.type
class GraphColumn:
    id: str
    name: str
    display_name: str
    sources: List[str]
    destinations: List[str]


@strawberry.type
class BaseTable:
    id: str
    name: str
    display_name: str
    namespace: str
    data_source: str
    x: int
    y: int
