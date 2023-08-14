import datetime
import time
from enum import Enum
from typing import List, Optional

from grai_graph.graph import BaseSourceSegment
from collections import defaultdict
import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from django.conf import settings
from django.db.models import Prefetch, Q
from django.db.models.query import QuerySet
from strawberry.scalars import JSON
from strawberry_django.filters import FilterLookup
from strawberry_django.pagination import OffsetPaginationInput
from strawberry.types import Info
from grai_graph.graph import BaseSourceSegment
from api.search import Search
from connections.models import Connection as ConnectionModel
from connections.models import Run as RunModel
from connections.types import Connector, ConnectorFilter
from installations.models import Branch as BranchModel
from installations.models import Commit as CommitModel
from installations.models import PullRequest as PullRequestModel
from installations.models import Repository as RepositoryModel
from lineage.filter import apply_table_filter, get_tags
from lineage.graph import GraphQuery
from lineage.graph_cache import GraphCache
from lineage.graph_types import BaseTable, GraphTable
from lineage.models import Edge as EdgeModel
from lineage.models import Event as EventModel
from lineage.models import Filter as FilterModel
from lineage.models import Node as NodeModel
from lineage.models import Source as SourceModel
from lineage.types import EdgeFilter, EdgeOrder, Filter, NodeFilter, NodeOrder
from notifications.models import Alert as AlertModel
from users.types import User, UserFilter
from workspaces.models import Membership as MembershipModel
from workspaces.models import Workspace as WorkspaceModel
from workspaces.models import WorkspaceAPIKey as WorkspaceAPIKeyModel
from workspaces.types import Organisation

from .pagination import DataWrapper, Pagination


@strawberry.enum
class RunAction(Enum):
    TESTS = RunModel.TESTS
    UPDATE = RunModel.UPDATE
    VALIDATE = RunModel.VALIDATE
    EVENTS = RunModel.EVENTS
    EVENTS_ALL = RunModel.EVENTS_ALL


@strawberry.enum
class EventStatus(Enum):
    SUCCESS = EventModel.SUCCESS
    ERROR = EventModel.ERROR
    CANCELLED = EventModel.CANCELLED


@strawberry.django.type(EventModel)
class Event:
    id: strawberry.auto
    date: strawberry.auto
    status: strawberry.auto
    connection: "Connection"
    metadata: JSON
    created_at: strawberry.auto


@strawberry.django.type(NodeModel, order=NodeOrder, filters=NodeFilter, pagination=True)
class Node:
    id: strawberry.auto
    namespace: strawberry.auto
    name: strawberry.auto
    display_name: strawberry.auto
    metadata: JSON
    is_active: strawberry.auto
    source_edges: List["Edge"]
    destination_edges: List["Edge"]

    # Columns
    @strawberry.django.field(
        prefetch_related=Prefetch(
            "source_edges",
            queryset=EdgeModel.objects.filter(metadata__grai__edge_type="TableToColumn").select_related("destination"),
            to_attr="edges_list",
        )
    )
    def columns(self) -> DataWrapper["Column"]:
        return DataWrapper[Column](list(set([edge.destination for edge in self.edges_list])))

    # Events
    @strawberry.field
    def events(
        self,
    ) -> Pagination[Event]:
        queryset = EventModel.objects.filter(nodes=self)

        return Pagination[Event](queryset=queryset)

    # Sources
    @strawberry.django.field
    def data_sources(
        self,
    ) -> Pagination["Source"]:
        queryset = SourceModel.objects.filter(nodes=self)

        return Pagination[Source](queryset=queryset)


@strawberry.django.type(EdgeModel, order=EdgeOrder, filters=EdgeFilter, pagination=True)
class Edge:
    id: strawberry.auto
    namespace: strawberry.auto
    name: strawberry.auto
    display_name: strawberry.auto
    source: Node = strawberry.django.field()
    destination: Node = strawberry.django.field()
    metadata: JSON
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto

    # Sources
    @strawberry.django.field
    def data_sources(
        self,
    ) -> Pagination["Source"]:
        queryset = SourceModel.objects.filter(edges=self)

        return Pagination[Source](queryset=queryset)


@strawberry.django.type(RunModel, order="RunOrder", pagination=True)
class Run:
    id: strawberry.auto
    connection: "Connection"
    status: strawberry.auto
    action: strawberry.auto
    metadata: JSON
    created_at: strawberry.auto
    updated_at: strawberry.auto
    started_at: Optional[datetime.datetime]
    finished_at: Optional[datetime.datetime]
    user: Optional[User]
    commit: Optional["Commit"]


@strawberry.input
class WorkspaceRunFilter:
    owner: Optional[str] = strawberry.UNSET
    repo: Optional[str] = strawberry.UNSET
    branch: Optional[str] = strawberry.UNSET
    action: Optional["RunAction"] = strawberry.UNSET


def apply_run_filters(queryset: QuerySet, filters: Optional[WorkspaceRunFilter] = strawberry.UNSET):
    if filters:
        q_filter = Q()

        if filters.owner:
            q_filter &= Q(
                commit__repository__owner=filters.owner,
                commit__repository__repo=filters.repo,
            )

        if filters.branch:
            q_filter &= Q(commit__branch__reference=filters.branch)

        if filters.action:
            q_filter &= Q(action=filters.action.value)

        queryset = queryset.filter(q_filter)

    return queryset


@strawberry.input
class WorkspaceTableFilter:
    filter: Optional[strawberry.ID] = strawberry.UNSET


@strawberry_django.ordering.order(RunModel)
class RunOrder:
    id: strawberry.auto
    created_at: strawberry.auto


@strawberry_django.filters.filter(ConnectionModel, lookups=True)
class ConnectionFilter:
    id: strawberry.auto
    namespace: strawberry.auto
    name: strawberry.auto
    source: "Source"
    connector: ConnectorFilter
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto
    created_by: UserFilter


@strawberry_django.ordering.order(ConnectionModel)
class ConnectionOrder:
    id: strawberry.auto
    namespace: strawberry.auto
    name: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry.django.type(ConnectionModel, order=ConnectionOrder, filters=ConnectionFilter, pagination=True)
class Connection:
    id: strawberry.auto
    connector: Connector
    source: "Source"
    namespace: strawberry.auto
    name: strawberry.auto
    metadata: JSON
    schedules: Optional[JSON]
    is_active: strawberry.auto
    temp: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto
    created_by: User

    # Runs
    @strawberry.field
    def runs(
        self,
        filters: Optional[WorkspaceRunFilter] = strawberry.UNSET,
        order: Optional[RunOrder] = strawberry.UNSET,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Run]:
        queryset = RunModel.objects.filter(connection=self)

        def apply_filters(queryset):
            return apply_run_filters(queryset, filters)

        return Pagination[Run](
            queryset=queryset,
            apply_filters=apply_filters,
            order=order,
            pagination=pagination,
        )

    # run: Run = strawberry.django.field
    @strawberry.django.field
    def run(self, id: strawberry.ID) -> "Run":
        return RunModel.objects.get(id=id)

    @strawberry.django.field
    def last_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(connection=self.id).order_by("-created_at").first()

    @strawberry.django.field
    def last_successful_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(connection=self.id, status="success").order_by("-created_at").first()

    # Events
    @strawberry.field
    def events(
        self,
    ) -> Pagination[Event]:
        queryset = EventModel.objects.filter(connection=self)

        return Pagination[Event](queryset=queryset)


@strawberry.input
class SourceNodeFilter:
    node_type: Optional[str] = strawberry.UNSET


@strawberry.input
class SourceConnectionFilter:
    temp: Optional[bool] = strawberry.UNSET


@strawberry.django.type(SourceModel)
class Source:
    id: strawberry.auto
    name: strawberry.auto
    priority: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto

    @strawberry.django.field
    def nodes(
        self,
        filters: Optional[SourceNodeFilter] = strawberry.UNSET,
        search: Optional[str] = strawberry.UNSET,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Node]:
        queryset = NodeModel.objects.filter(data_sources=self)

        if filters:
            if filters.node_type:
                queryset = queryset.filter(metadata__grai__node_type=filters.node_type)

        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) | Q(name__icontains=search) | Q(display_name__icontains=search)
            )

        return Pagination[Node](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def edges(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Edge]:
        queryset = EdgeModel.objects.filter(data_sources=self)

        return Pagination[Edge](queryset=queryset, pagination=pagination)

    @strawberry.field
    def connections(
        self,
        filters: Optional[SourceConnectionFilter] = strawberry.UNSET,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Connection]:
        queryset = ConnectionModel.objects.filter(source=self)

        if filters:
            if filters.temp is not strawberry.UNSET:
                queryset = queryset.filter(temp=filters.temp)

        return Pagination[Connection](queryset=queryset, pagination=pagination)


@strawberry.django.type(NodeModel, order=NodeOrder, filters=NodeFilter, pagination=True)
class Column(Node):
    @strawberry.django.field
    def requirements_edges(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Edge"]:
        queryset = EdgeModel.objects.filter(source=self).filter(metadata__grai__edge_type="ColumnToColumn")

        return Pagination[Edge](queryset=queryset, pagination=pagination)


@strawberry.django.type(NodeModel, order=NodeOrder, filters=NodeFilter, pagination=True)
class Table(Node):
    @strawberry.django.field(
        prefetch_related=Prefetch(
            "source_edges",
            queryset=EdgeModel.objects.filter(metadata__grai__edge_type="TableToColumn").select_related("destination"),
            to_attr="edges_list",
        )
    )
    def columns(self) -> DataWrapper[Column]:
        return DataWrapper[Column](list(set([edge.destination for edge in self.edges_list])))

    @strawberry.django.field(
        prefetch_related=(
            Prefetch(
                "source_edges",
                queryset=EdgeModel.objects.exclude(metadata__grai__edge_type="TableToColumn").select_related(
                    "destination"
                ),
                to_attr="sources_list",
            ),
            Prefetch(
                "source_edges",
                queryset=EdgeModel.objects.filter(metadata__grai__edge_type="TableToColumn")
                .select_related("destination")
                .prefetch_related(
                    Prefetch(
                        "destination__source_edges",
                        queryset=EdgeModel.objects.exclude(metadata__grai__edge_type="TableToColumn")
                        .select_related("destination")
                        .prefetch_related(
                            Prefetch(
                                "destination__destination_edges",
                                queryset=EdgeModel.objects.filter(
                                    metadata__grai__edge_type="TableToColumn"
                                ).select_related("source"),
                                to_attr="tables",
                            )
                        ),
                        to_attr="sources_list",
                    ),
                    Prefetch(
                        "destination__destination_edges",
                        queryset=EdgeModel.objects.exclude(metadata__grai__edge_type="TableToColumn")
                        .select_related("source")
                        .prefetch_related(
                            Prefetch(
                                "source__destination_edges",
                                queryset=EdgeModel.objects.filter(
                                    metadata__grai__edge_type="TableToColumn"
                                ).select_related("source"),
                                to_attr="tables",
                            )
                        ),
                        to_attr="destination_list",
                    ),
                ),
                to_attr="columns",
            ),
        )
    )
    def source_tables(self) -> DataWrapper["Table"]:
        tables = []

        for source in self.sources_list:
            tables.append(source.destination)

        for column in self.columns:
            for source in column.destination.sources_list:
                for table in source.destination.tables:
                    tables.append(table.source)

        return DataWrapper["Table"](list(set(tables)))

    @strawberry.django.field(
        prefetch_related=(
            Prefetch(
                "destination_edges",
                queryset=EdgeModel.objects.exclude(metadata__grai__edge_type="TableToColumn").select_related("source"),
                to_attr="destinations_list",
            ),
            Prefetch(
                "source_edges",
                queryset=EdgeModel.objects.filter(metadata__grai__edge_type="TableToColumn")
                .select_related("destination")
                .prefetch_related(
                    Prefetch(
                        "destination__source_edges",
                        queryset=EdgeModel.objects.exclude(metadata__grai__edge_type="TableToColumn")
                        .select_related("destination")
                        .prefetch_related(
                            Prefetch(
                                "destination__destination_edges",
                                queryset=EdgeModel.objects.filter(
                                    metadata__grai__edge_type="TableToColumn"
                                ).select_related("source"),
                                to_attr="tables",
                            )
                        ),
                        to_attr="sources_list",
                    ),
                    Prefetch(
                        "destination__destination_edges",
                        queryset=EdgeModel.objects.exclude(metadata__grai__edge_type="TableToColumn")
                        .select_related("source")
                        .prefetch_related(
                            Prefetch(
                                "source__destination_edges",
                                queryset=EdgeModel.objects.filter(
                                    metadata__grai__edge_type="TableToColumn"
                                ).select_related("source"),
                                to_attr="tables",
                            )
                        ),
                        to_attr="destination_list",
                    ),
                ),
                to_attr="columns2",
            ),
        )
    )
    def destination_tables(self) -> DataWrapper["Table"]:
        tables = []

        for destination in self.destinations_list:
            tables.append(destination.source)

        for column in self.columns2:
            for destination in column.destination.destination_list:
                for table in destination.source.tables:
                    tables.append(table.source)

        return DataWrapper["Table"](list(set(tables)))


@strawberry.input
class GraphFilter:
    source_id: Optional[strawberry.ID] = strawberry.UNSET
    table_id: Optional[strawberry.ID] = strawberry.UNSET
    edge_id: Optional[strawberry.ID] = strawberry.UNSET
    n: Optional[int] = strawberry.UNSET
    filters: Optional[List[strawberry.ID]] = strawberry.UNSET
    min_x: Optional[int] = strawberry.UNSET
    max_x: Optional[int] = strawberry.UNSET
    min_y: Optional[int] = strawberry.UNSET
    max_y: Optional[int] = strawberry.UNSET


@strawberry.input
class WorkspaceRepositoryFilter:
    type: Optional[str] = strawberry.UNSET
    owner: Optional[str] = strawberry.UNSET
    repo: Optional[str] = strawberry.UNSET
    installed: Optional[bool] = strawberry.UNSET


@strawberry.input
class StringFilter:
    equals: Optional[str] = strawberry.UNSET
    contains: Optional[List[str]] = strawberry.UNSET


@strawberry.input
class WorkspaceEdgeFilter:
    edge_type: Optional[StringFilter] = strawberry.UNSET


@strawberry.input
class WorkspaceNodeFilter:
    node_type: Optional[StringFilter] = strawberry.UNSET


@strawberry_django.filters.filter(WorkspaceModel)
class WorkspaceFilter:
    id: strawberry.auto
    name: FilterLookup[str]
    memberships: FilterLookup["MembershipFilter"]


@strawberry_django.ordering.order(WorkspaceModel)
class WorkspaceOrder:
    id: strawberry.auto
    name: strawberry.auto


@strawberry.django.type(WorkspaceModel, order=WorkspaceOrder, filters=WorkspaceFilter, pagination=True)
class Workspace:
    id: strawberry.auto
    name: strawberry.auto

    created_at: strawberry.auto
    updated_at: strawberry.auto

    organisation: Organisation

    # Nodes
    @strawberry.django.field
    def nodes(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
        search: Optional[str] = strawberry.UNSET,
        filter: Optional[WorkspaceNodeFilter] = strawberry.UNSET,
    ) -> Pagination["Node"]:
        queryset = NodeModel.objects.filter(workspace=self)

        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) | Q(name__icontains=search) | Q(display_name__icontains=search)
            )

        if filter:
            if filter.node_type:
                if filter.node_type.equals:
                    queryset = queryset.filter(metadata__grai__node_type=filter.node_type.equals)
                if filter.node_type.contains:
                    queryset = queryset.filter(metadata__grai__node_type__in=filter.node_type.contains)

        return Pagination[Node](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def node(self, id: strawberry.ID) -> Node:
        return NodeModel.objects.filter(
            id=id,
            workspace=self,
        )

    # Edges
    @strawberry.django.field
    def edges(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
        search: Optional[str] = strawberry.UNSET,
        filter: Optional[WorkspaceEdgeFilter] = strawberry.UNSET,
    ) -> Pagination["Edge"]:
        queryset = EdgeModel.objects.filter(workspace=self)

        if search:
            queryset = queryset.filter(
                Q(id__icontains=search)
                | Q(name__icontains=search)
                | Q(destination__name__icontains=search)
                | Q(source__name__icontains=search)
            )

        if filter:
            if filter.edge_type:
                if filter.edge_type.equals:
                    queryset = queryset.filter(metadata__grai__edge_type=filter.edge_type.equals)
                if filter.edge_type.contains:
                    queryset = queryset.filter(metadata__grai__edge_type__in=filter.edge_type.contains)

        return Pagination[Edge](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def edge(self, id: strawberry.ID) -> Edge:
        return EdgeModel.objects.get(id=id)

    # Connections
    @strawberry.django.field
    def connections(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Connection]:
        queryset = ConnectionModel.objects.filter(workspace=self, temp=False)

        return Pagination[Connection](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def connection(self, id: strawberry.ID) -> Connection:
        return ConnectionModel.objects.get(id=id)

    # Runs
    @strawberry.field
    def runs(
        self,
        filters: Optional[WorkspaceRunFilter] = strawberry.UNSET,
        order: Optional[RunOrder] = strawberry.UNSET,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Run]:
        queryset = RunModel.objects.filter(workspace=self)

        def apply_filters(queryset):
            return apply_run_filters(queryset, filters)

        return Pagination[Run](
            queryset=queryset,
            apply_filters=apply_filters,
            order=order,
            pagination=pagination,
        )

    @strawberry.django.field
    def run(self, id: strawberry.ID) -> "Run":
        return RunModel.objects.get(id=id)

    # Memberships
    @strawberry.django.field
    def memberships(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Membership"]:
        queryset = MembershipModel.objects.filter(workspace=self).filter(hidden=False)

        return Pagination[Membership](queryset=queryset, pagination=pagination)

    # Api Keys
    @strawberry.django.field
    def api_keys(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["WorkspaceAPIKey"]:
        queryset = WorkspaceAPIKeyModel.objects.filter(workspace=self)

        return Pagination[WorkspaceAPIKey](queryset=queryset, pagination=pagination)

    # Tables
    @strawberry.django.field
    async def tables(
        self,
        filters: Optional[WorkspaceTableFilter] = strawberry.UNSET,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
        search: Optional[str] = strawberry.UNSET,
    ) -> Pagination[Table]:
        queryset = NodeModel.objects.filter(workspace=self, metadata__grai__node_type="Table")

        if search:
            queryset = queryset.filter(name__icontains=search)

        if filters and filters.filter:
            filter = await FilterModel.objects.aget(id=filters.filter)

            filteredQueryset = await apply_table_filter(queryset, filter)

            return Pagination[Table](
                queryset=queryset,
                filteredQueryset=filteredQueryset,
                pagination=pagination,
            )

        return Pagination[Table](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def table(self, id: strawberry.ID) -> Table:
        return NodeModel.objects.filter(id=id, workspace=self, metadata__grai__node_type="Table")

    # Repositories
    @strawberry.django.field
    def repositories(
        self,
        filters: Optional[WorkspaceRepositoryFilter] = strawberry.UNSET,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Repository"]:
        queryset = RepositoryModel.objects.filter(workspace=self)

        def apply_filters(queryset: QuerySet) -> QuerySet:
            if filters:
                q_filter = Q()

                if filters.type:
                    q_filter &= Q(type=filters.type)

                if filters.owner:
                    q_filter &= Q(owner=filters.owner)

                if filters.repo:
                    q_filter &= Q(repo=filters.repo)

                if filters.installed is not strawberry.UNSET:
                    q_filter &= Q(installation_id__isnull=not filters.installed)

                return queryset.filter(q_filter)

            return queryset

        return Pagination[Repository](queryset=queryset, apply_filters=apply_filters, pagination=pagination)

    @strawberry.django.field
    def repository(
        self,
        id: Optional[strawberry.ID] = None,
        type: Optional[str] = strawberry.UNSET,
        owner: Optional[str] = strawberry.UNSET,
        repo: Optional[str] = strawberry.UNSET,
    ) -> "Repository":
        return (
            RepositoryModel.objects.get(id=id)
            if id is not None
            else RepositoryModel.objects.get(workspace=self, type=type, owner=owner, repo=repo)
        )

    # Branches
    @strawberry.django.field
    def branches(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Branch"]:
        queryset = BranchModel.objects.filter(workspace=self)

        return Pagination["Branch"](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def branch(
        self,
        id: Optional[strawberry.ID] = None,
        reference: Optional[str] = strawberry.UNSET,
    ) -> "Branch":
        return (
            BranchModel.objects.get(id=id)
            if id is not None
            else BranchModel.objects.get(workspace=self, reference=reference)
        )

    # Pull Requests
    @strawberry.django.field
    def pull_requests(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["PullRequest"]:
        queryset = PullRequestModel.objects.filter(workspace=self)

        return Pagination[PullRequest](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def pull_request(
        self,
        id: Optional[strawberry.ID] = None,
        reference: Optional[str] = strawberry.UNSET,
    ) -> "PullRequest":
        return (
            PullRequestModel.objects.get(id=id)
            if id is not None
            else PullRequestModel.objects.get(workspace=self, reference=reference)
        )

    # Commits
    @strawberry.django.field
    def commits(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Commit"]:
        queryset = CommitModel.objects.filter(workspace=self)

        return Pagination[Commit](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def commit(
        self,
        id: Optional[strawberry.ID] = None,
        reference: Optional[str] = strawberry.UNSET,
    ) -> "Commit":
        return (
            CommitModel.objects.get(id=id)
            if id is not None
            else CommitModel.objects.get(workspace=self, reference=reference)
        )

    # Alerts
    @strawberry.django.field
    def alerts(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Alert"]:
        queryset = AlertModel.objects.filter(workspace=self)

        return Pagination[Alert](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def alert(self, id: strawberry.ID) -> "Alert":
        return AlertModel.objects.get(id=id)

    # Algolia search key
    @strawberry.django.field
    def search_key(self) -> str:
        api_key = settings.ALGOLIA_SEARCH_KEY

        if not api_key:
            raise Exception("Algolia not setup")

        client = Search()

        valid_until = int(time.time()) + 3600

        return client.generate_secured_api_key(
            api_key,
            {
                "filters": f"workspace_id:{str(self.id)}",
                "validUntil": valid_until,
                "restrictIndices": "main",
            },
        )

    # Filters
    @strawberry.field
    def filters(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
        search: Optional[str] = strawberry.UNSET,
    ) -> Pagination[Filter]:
        queryset = FilterModel.objects.filter(workspace=self)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return Pagination[Filter](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def filter(self, id: strawberry.ID) -> "Filter":
        return FilterModel.objects.get(id=id)

    # Tags
    @strawberry.field
    async def tags(
        self,
    ) -> DataWrapper[str]:
        data = await sync_to_async(get_tags)(self)

        return DataWrapper[str](data=data)

    # Namespaces
    @strawberry.field
    async def namespaces(self) -> DataWrapper[str]:
        namespaces = await sync_to_async(list)(
            NodeModel.objects.filter(workspace=self).values_list("namespace", flat=True).distinct()
        )

        print(namespaces)

        return DataWrapper(namespaces)

    # Graph
    @strawberry.django.field
    async def graph(
        self,
        filters: Optional[GraphFilter] = strawberry.UNSET,
    ) -> List[GraphTable]:
        graph = GraphCache(workspace=self)

        query = GraphQuery([], {})
        query.match("(table:Table)")

        if filters and filters.source_id:
            return graph.get_source_filtered_graph_result(filters.source_id, filters.n)

        if filters and filters.table_id:
            return graph.get_table_filtered_graph_result(filters.table_id, filters.n)

        if filters and filters.edge_id:
            return graph.get_edge_filtered_graph_result(filters.edge_id, filters.n)

        if filters and filters.min_x is not None and filters.max_x is not strawberry.UNSET:
            graph.filter_by_range(filters.min_x, filters.max_x, filters.min_y, filters.max_y, query)

        if filters and filters.filters:
            filter_list = await sync_to_async(FilterModel.objects.filter(id__in=filters.filters).all)()

            await sync_to_async(graph.filter_by_filters)(filter_list, query)

        return graph.get_graph_result(query=query)

    # Graph Tables
    @strawberry.django.field
    async def graph_tables(
        self,
        search: Optional[str] = strawberry.UNSET,
    ) -> List[BaseTable]:
        def get_tables(search: Optional[str]) -> List[Table]:
            def get_words(word: str) -> List[str]:
                from django.db import connection

                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM unique_lexeme WHERE levenshtein_less_equal(word, %s, 2) < 3",
                        [word],
                    )
                    rows = cursor.fetchall()

                return list([item[0] for item in rows])

            result = []

            for word in search.replace("_", " ").replace(".", " ").strip().split(" "):
                result += get_words(word)

            search_string = " ".join(result)

            return list(
                NodeModel.objects.raw(
                    """
                    SELECT *
                    FROM lineage_node
                    WHERE workspace_id=%s
                    AND metadata->'grai'->>'node_type'='Table'
                    AND ts_rank(search, websearch_to_tsquery('simple', replace(replace(%s, ' ', ' or '), '.', ' or '))) > 0
                    ORDER BY ts_rank(search, websearch_to_tsquery('simple', replace(replace(%s, ' ', ' or '), '.', ' or '))) DESC""",
                    [self.id, search_string, search_string],
                )
            )

        graph = GraphCache(workspace=self)

        ids = None

        if search:
            tables = await sync_to_async(get_tables)(search)

            ids = [table.id for table in tables]

        return graph.get_tables(ids=ids)

    # Sources
    @strawberry.field
    def sources(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Source]:
        queryset = SourceModel.objects.filter(workspace=self)

        return Pagination[Source](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def source(self, id: strawberry.ID) -> Source:
        return SourceModel.objects.get(id=id)

    # Source Graph
    @strawberry.field
    def source_graph(self) -> JSON:
        def fetch_source_graph(workspace: WorkspaceModel):
            nodes = (
                NodeModel.objects.filter(workspace=workspace, is_active=True)
                .prefetch_related("data_sources")
                .values("id", "data_sources__name")
            )
            grouped_nodes = defaultdict(list)
            for result in nodes:
                grouped_nodes[result["id"]].append(result["data_sources__name"])

            nodes = grouped_nodes

            edges = defaultdict(list)
            for edge in EdgeModel.objects.filter(workspace=workspace, is_active=True).values("source", "destination"):
                edges[edge["source"]].append(edge["destination"])

            # I can convert this into an explicit SQL queries to avoid loading the entire graph if needed.
            segmentation = BaseSourceSegment(node_source_map=nodes, edge_map=edges)

            result = segmentation.cover_edge_map.copy()
            for source in segmentation.covering_set:
                result.setdefault(source, [])

            return result

        return sync_to_async(fetch_source_graph)(self)


@strawberry_django.filters.filter(MembershipModel, lookups=True)
class MembershipFilter:
    id: strawberry.auto
    role: strawberry.auto
    is_active: strawberry.auto
    user: UserFilter
    workspace: WorkspaceFilter
    created_at: strawberry.auto


@strawberry_django.ordering.order(MembershipModel)
class MembershipOrder:
    id: strawberry.auto
    role: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto


@strawberry.django.type(MembershipModel, order=MembershipOrder, filters=MembershipFilter, pagination=True)
class Membership:
    id: strawberry.auto
    role: strawberry.auto
    user: User
    workspace: Workspace
    is_active: strawberry.auto
    created_at: strawberry.auto


@strawberry_django.filters.filter(WorkspaceAPIKeyModel, lookups=True)
class WorkspaceAPIKeyFilter:
    id: strawberry.auto
    name: strawberry.auto
    revoked: strawberry.auto
    expiry_date: strawberry.auto
    created: strawberry.auto


@strawberry_django.ordering.order(WorkspaceAPIKeyModel)
class WorkspaceAPIKeyOrder:
    id: strawberry.auto
    name: strawberry.auto
    created: strawberry.auto


@strawberry.django.type(
    WorkspaceAPIKeyModel,
    order=WorkspaceAPIKeyOrder,
    filters=WorkspaceAPIKeyFilter,
    pagination=True,
    only=["id", "revoked"],
)
class WorkspaceAPIKey:
    id: strawberry.auto
    name: strawberry.auto
    prefix: strawberry.auto
    revoked: strawberry.auto
    expiry_date: Optional[datetime.datetime]
    # has_expired: strawberry.auto
    created: strawberry.auto
    created_by: User


@strawberry.type
class KeyResult:
    key: str
    api_key: WorkspaceAPIKey


@strawberry.type
class BasicResult:
    success: bool


@strawberry.django.type(RepositoryModel)
class Repository:
    id: strawberry.auto
    workspace: Workspace
    type: strawberry.auto
    owner: strawberry.auto
    repo: strawberry.auto

    # Pull Requests
    @strawberry.django.field
    def pull_requests(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["PullRequest"]:
        queryset = PullRequestModel.objects.filter(repository=self)

        return Pagination[PullRequest](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def pull_request(
        self,
        id: Optional[strawberry.ID] = None,
        reference: Optional[str] = strawberry.UNSET,
    ) -> "PullRequest":
        return (
            PullRequestModel.objects.get(id=id)
            if id is not None
            else PullRequestModel.objects.get(repository=self, reference=reference)
        )

    # Branches
    @strawberry.django.field
    def branches(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Branch"]:
        queryset = BranchModel.objects.filter(repository=self)

        return Pagination["Branch"](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def branch(
        self,
        id: Optional[strawberry.ID] = None,
        reference: Optional[str] = strawberry.UNSET,
    ) -> "Branch":
        return (
            BranchModel.objects.get(id=id)
            if id is not None
            else BranchModel.objects.get(repository=self, reference=reference)
        )

    # Commits
    @strawberry.django.field
    def commits(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Commit"]:
        queryset = CommitModel.objects.filter(repository=self)

        return Pagination[Commit](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def commit(
        self,
        id: Optional[strawberry.ID] = None,
        reference: Optional[str] = strawberry.UNSET,
    ) -> "Commit":
        return (
            CommitModel.objects.get(id=id)
            if id is not None
            else CommitModel.objects.get(repository=self, reference=reference)
        )


@strawberry.django.type(BranchModel)
class Branch:
    id: strawberry.auto
    reference: strawberry.auto
    repository: "Repository"

    # Pull Requests
    @strawberry.django.field
    def pull_requests(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["PullRequest"]:
        queryset = PullRequestModel.objects.filter(branch=self)

        return Pagination[PullRequest](queryset=queryset, pagination=pagination)

    # Commits
    @strawberry.django.field
    def commits(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Commit"]:
        queryset = CommitModel.objects.filter(branch=self)

        return Pagination[Commit](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def last_commit(self) -> Optional["Commit"]:
        return CommitModel.objects.filter(branch=self.id).order_by("-created_at").first()


@strawberry.django.type(PullRequestModel)
class PullRequest:
    id: strawberry.auto
    reference: strawberry.auto
    title: Optional[str]
    repository: "Repository"
    branch: "Branch"

    # Commits
    @strawberry.django.field
    def commits(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Commit"]:
        queryset = CommitModel.objects.filter(pull_request=self)

        return Pagination[Commit](queryset=queryset, pagination=pagination)

    @strawberry.django.field
    def last_commit(self) -> Optional["Commit"]:
        return CommitModel.objects.filter(pull_request=self.id).order_by("-created_at").first()


@strawberry.django.type(CommitModel)
class Commit:
    id: strawberry.auto
    reference: strawberry.auto
    title: Optional[str]
    repository: "Repository"
    branch: "Branch"
    pull_request: Optional["PullRequest"]
    created_at: strawberry.auto

    # Runs
    @strawberry.field
    def runs(
        self,
        filters: Optional[WorkspaceRunFilter] = strawberry.UNSET,
        order: Optional[RunOrder] = strawberry.UNSET,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Run]:
        queryset = RunModel.objects.filter(commit=self)

        def apply_filters(queryset):
            return apply_run_filters(queryset, filters)

        return Pagination[Run](
            queryset=queryset,
            apply_filters=apply_filters,
            order=order,
            pagination=pagination,
        )

    @strawberry.django.field
    def last_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(commit=self.id).order_by("-created_at").first()

    @strawberry.django.field
    def last_successful_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(commit=self.id, status="success").order_by("-created_at").first()


@strawberry.django.type(AlertModel)
class Alert:
    id: strawberry.auto
    name: strawberry.auto
    channel: strawberry.auto
    channel_metadata: JSON
    triggers: JSON
    is_active: strawberry.auto
    created_at: strawberry.auto
