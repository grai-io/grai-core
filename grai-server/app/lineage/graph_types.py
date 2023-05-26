from typing import List, Optional
import strawberry


@strawberry.type
class GraphTable:
    def __init__(
        self,
        id: str,
        name: str,
        display_name: str,
        namespace: str,
        data_source: str,
        columns: List["GraphColumn"],
        sources: List[str],
        destinations: List[str],
        table_destinations: Optional[List[str]] = None,
        table_sources: Optional[List[str]] = None,
    ):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.namespace = namespace
        self.data_source = data_source
        self.columns = columns
        self.sources = sources
        self.destinations = destinations
        self.table_destinations = table_destinations
        self.table_sources = table_sources

    id: str
    name: str
    display_name: str
    namespace: str
    data_source: str
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
