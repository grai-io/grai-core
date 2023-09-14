from typing import List, Optional

import strawberry


@strawberry.type
class TableEdge:
    edge_id: str
    table_id: str


@strawberry.type
class ColumnEdge:
    edge_id: str
    column_id: str


@strawberry.type
class GraphTable:
    id: str
    name: str
    display_name: str
    namespace: str
    data_source: Optional[str]
    x: float
    y: float
    columns: List["GraphColumn"]
    sources: List[str]
    destinations: List[TableEdge]
    table_destinations: Optional[List[str]]
    table_sources: Optional[List[str]]


@strawberry.type
class GraphColumn:
    id: str
    name: str
    display_name: str
    sources: List[str]
    destinations: List[ColumnEdge]


@strawberry.type
class BaseTable:
    id: str
    name: str
    display_name: str
    namespace: str
    data_source: Optional[str]
    x: float
    y: float
