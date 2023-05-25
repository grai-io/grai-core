import datetime
import time
from enum import Enum
from typing import List, Optional
from xml.dom import NodeFilter

import strawberry
import strawberry_django
from django.conf import settings
from django.db.models import Prefetch, Q
from django.db.models.query import QuerySet
from notifications.models import Alert as AlertModel
from strawberry.scalars import JSON
from strawberry_django.filters import FilterLookup
from strawberry_django.pagination import OffsetPaginationInput
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from api.search import Search
from connections.models import Connection as ConnectionModel
from connections.models import Run as RunModel
from connections.types import Connector, ConnectorFilter
from installations.models import Branch as BranchModel
from installations.models import Commit as CommitModel
from installations.models import PullRequest as PullRequestModel
from installations.models import Repository as RepositoryModel
from lineage.filter import apply_table_filter, get_tags
from lineage.graph import (
    get_edge_filtered_graph_result,
    get_filtered_graph_result,
    get_graph_result,
)
from lineage.models import Edge as EdgeModel
from lineage.models import Filter as FilterModel
from lineage.models import Node as NodeModel
from lineage.types import Edge, Filter, GraphTable, Node, NodeFilter, NodeOrder
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


@gql.django.type(RunModel, order="RunOrder", pagination=True)
class Run:
    id: auto
    connection: "Connection"
    status: auto
    action: RunAction
    metadata: JSON
    created_at: auto
    updated_at: auto
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
            q_filter &= Q(commit__repository__owner=filters.owner, commit__repository__repo=filters.repo)

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
    id: auto
    created_at: auto


@gql.django.filters.filter(ConnectionModel, lookups=True)
class ConnectionFilter:
    id: auto
    namespace: auto
    name: auto
    connector: ConnectorFilter
    is_active: auto
    created_at: auto
    updated_at: auto
    created_by: UserFilter


@strawberry_django.ordering.order(ConnectionModel)
class ConnectionOrder:
    id: auto
    namespace: auto
    name: auto
    is_active: auto
    created_at: auto
    updated_at: auto


@gql.django.type(ConnectionModel, order=ConnectionOrder, filters=ConnectionFilter, pagination=True)
class Connection:
    id: auto
    connector: Connector
    namespace: auto
    name: auto
    metadata: JSON
    schedules: Optional[JSON]
    is_active: auto
    temp: auto
    created_at: auto
    updated_at: auto
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

        return Pagination[Run](queryset=queryset, apply_filters=apply_filters, order=order, pagination=pagination)

    # run: Run = strawberry.django.field
    @gql.django.field
    def run(self, id: strawberry.ID) -> "Run":
        return RunModel.objects.get(id=id)

    @gql.django.field
    def last_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(connection=self.id).order_by("-created_at").first()

    @gql.django.field
    def last_successful_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(connection=self.id, status="success").order_by("-created_at").first()


@gql.django.type(NodeModel, order=NodeOrder, filters=NodeFilter, pagination=True)
class Column(Node):
    @gql.django.field
    def requirements_edges(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Edge]:
        queryset = EdgeModel.objects.filter(source=self).filter(metadata__grai__edge_type="ColumnToColumn")

        return Pagination[Edge](queryset=queryset, pagination=pagination)


@gql.django.type(NodeModel, order=NodeOrder, filters=NodeFilter, pagination=True)
class Table(Node):
    @gql.django.field(
        prefetch_related=Prefetch(
            "source_edges",
            queryset=EdgeModel.objects.filter(metadata__grai__edge_type="TableToColumn").select_related("destination"),
            to_attr="edges_list",
        )
    )
    def columns(self) -> DataWrapper[Column]:
        return DataWrapper[Column](list(set([edge.destination for edge in self.edges_list])))

    @gql.django.field(
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

    @gql.django.field(
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
class WorkspaceRepositoryFilter:
    type: Optional[str] = strawberry.UNSET
    owner: Optional[str] = strawberry.UNSET
    repo: Optional[str] = strawberry.UNSET
    installed: Optional[bool] = strawberry.UNSET


@gql.django.filters.filter(WorkspaceModel)
class WorkspaceFilter:
    id: auto
    name: FilterLookup[str]
    memberships: FilterLookup["MembershipFilter"]


@strawberry_django.ordering.order(WorkspaceModel)
class WorkspaceOrder:
    id: auto
    name: auto


@gql.django.type(WorkspaceModel, order=WorkspaceOrder, filters=WorkspaceFilter, pagination=True)
class Workspace:
    id: auto
    name: auto

    created_at: auto
    updated_at: auto

    organisation: Organisation

    # Nodes
    @gql.django.field
    def nodes(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Node"]:
        queryset = NodeModel.objects.filter(workspace=self)

        return Pagination[Node](queryset=queryset, pagination=pagination)

    @gql.django.field
    def node(self, id: strawberry.ID) -> Node:
        return NodeModel.objects.get(id=id)

    # Edges
    @gql.django.field
    def edges(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Edge"]:
        queryset = EdgeModel.objects.filter(workspace=self)

        return Pagination[Edge](queryset=queryset, pagination=pagination)

    @gql.django.field
    def edge(self, id: strawberry.ID) -> Edge:
        return EdgeModel.objects.get(id=id)

    # Connections
    @gql.django.field
    def connections(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Connection]:
        queryset = ConnectionModel.objects.filter(workspace=self, temp=False)

        return Pagination[Connection](queryset=queryset, pagination=pagination)

    @gql.django.field
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

        return Pagination[Run](queryset=queryset, apply_filters=apply_filters, order=order, pagination=pagination)

    @gql.django.field
    def run(self, id: strawberry.ID) -> "Run":
        return RunModel.objects.get(id=id)

    # Memberships
    @gql.django.field
    def memberships(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Membership"]:
        queryset = MembershipModel.objects.filter(workspace=self).filter(hidden=False)

        return Pagination[Membership](queryset=queryset, pagination=pagination)

    # Api Keys
    @gql.django.field
    def api_keys(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["WorkspaceAPIKey"]:
        queryset = WorkspaceAPIKeyModel.objects.filter(workspace=self)

        return Pagination[WorkspaceAPIKey](queryset=queryset, pagination=pagination)

    # Tables
    @gql.django.field
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

            return Pagination[Table](queryset=queryset, filteredQueryset=filteredQueryset, pagination=pagination)

        return Pagination[Table](queryset=queryset, pagination=pagination)

    @gql.django.field
    def table(self, id: strawberry.ID) -> Table:
        return NodeModel.objects.filter(id=id, workspace=self, metadata__grai__node_type="Table")

    # Other edges
    @gql.django.field
    def other_edges(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Edge]:
        queryset = EdgeModel.objects.filter(workspace=self).filter(
            metadata__grai__edge_type__in=["TableToTable", "ColumnToColumn"]
        )

        print(queryset.query)

        return Pagination[Edge](queryset=queryset, pagination=pagination)

    # Repositories
    @gql.django.field
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

    @gql.django.field
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
    @gql.django.field
    def branches(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Branch"]:
        queryset = BranchModel.objects.filter(workspace=self)

        return Pagination["Branch"](queryset=queryset, pagination=pagination)

    @gql.django.field
    def branch(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = strawberry.UNSET) -> "Branch":
        return (
            BranchModel.objects.get(id=id)
            if id is not None
            else BranchModel.objects.get(workspace=self, reference=reference)
        )

    # Pull Requests
    @gql.django.field
    def pull_requests(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["PullRequest"]:
        queryset = PullRequestModel.objects.filter(workspace=self)

        return Pagination[PullRequest](queryset=queryset, pagination=pagination)

    @gql.django.field
    def pull_request(
        self, id: Optional[strawberry.ID] = None, reference: Optional[str] = strawberry.UNSET
    ) -> "PullRequest":
        return (
            PullRequestModel.objects.get(id=id)
            if id is not None
            else PullRequestModel.objects.get(workspace=self, reference=reference)
        )

    # Commits
    @gql.django.field
    def commits(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Commit"]:
        queryset = CommitModel.objects.filter(workspace=self)

        return Pagination[Commit](queryset=queryset, pagination=pagination)

    @gql.django.field
    def commit(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = strawberry.UNSET) -> "Commit":
        return (
            CommitModel.objects.get(id=id)
            if id is not None
            else CommitModel.objects.get(workspace=self, reference=reference)
        )

    # Alerts
    @gql.django.field
    def alerts(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Alert"]:
        queryset = AlertModel.objects.filter(workspace=self)

        return Pagination[Alert](queryset=queryset, pagination=pagination)

    @gql.django.field
    def alert(self, id: strawberry.ID) -> "Alert":
        return AlertModel.objects.get(id=id)

    # Algolia search key
    @gql.django.field
    def search_key(self) -> str:
        api_key = settings.ALGOLIA_SEARCH_KEY

        if not api_key:
            raise Exception("Alogia not setup")

        client = Search()

        valid_until = int(time.time()) + 3600

        return client.generate_secured_api_key(
            api_key,
            {"filters": f"workspace_id:{str(self.id)}", "validUntil": valid_until, "restrictIndices": "main"},
        )

    # Filters
    @strawberry.field
    def filters(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination[Filter]:
        queryset = FilterModel.objects.filter(workspace=self)

        return Pagination[Filter](queryset=queryset, pagination=pagination)

    @gql.django.field
    def filter(self, id: strawberry.ID) -> "Filter":
        return FilterModel.objects.get(id=id)

    # Tags
    @strawberry.field
    def tags(
        self,
    ) -> DataWrapper[str]:
        data = get_tags(self)

        return DataWrapper[str](data=data)

    @gql.django.field
    def graph(
        self,
        table_id: Optional[strawberry.ID] = strawberry.UNSET,
        n: Optional[int] = strawberry.UNSET,
        edge_id: Optional[strawberry.ID] = strawberry.UNSET,
    ) -> List["GraphTable"]:
        if table_id:
            return get_filtered_graph_result(self.id, table_id, n)

        if edge_id:
            return get_edge_filtered_graph_result(self.id, edge_id, n)

        return get_graph_result(self.id)


@gql.django.filters.filter(MembershipModel, lookups=True)
class MembershipFilter:
    id: auto
    role: auto
    is_active: auto
    user: UserFilter
    workspace: WorkspaceFilter
    created_at: auto


@strawberry_django.ordering.order(MembershipModel)
class MembershipOrder:
    id: auto
    role: auto
    is_active: auto
    created_at: auto


@gql.django.type(MembershipModel, order=MembershipOrder, filters=MembershipFilter, pagination=True)
class Membership:
    id: auto
    role: auto
    user: User
    workspace: Workspace
    is_active: auto
    created_at: auto


@gql.django.filters.filter(WorkspaceAPIKeyModel, lookups=True)
class WorkspaceAPIKeyFilter:
    id: auto
    name: auto
    revoked: auto
    expiry_date: auto
    created: auto


@strawberry_django.ordering.order(WorkspaceAPIKeyModel)
class WorkspaceAPIKeyOrder:
    id: auto
    name: auto
    created: auto


@gql.django.type(
    WorkspaceAPIKeyModel,
    order=WorkspaceAPIKeyOrder,
    filters=WorkspaceAPIKeyFilter,
    pagination=True,
    only=["id", "revoked"],
)
class WorkspaceAPIKey:
    id: auto
    name: auto
    prefix: auto
    revoked: auto
    expiry_date: Optional[datetime.datetime]
    # has_expired: auto
    created: auto
    created_by: User


@gql.type
class KeyResult:
    key: str
    api_key: WorkspaceAPIKey


@gql.type
class BasicResult:
    success: bool


@gql.django.type(RepositoryModel)
class Repository:
    id: auto
    workspace: Workspace
    type: auto
    owner: auto
    repo: auto

    # Pull Requests
    @gql.django.field
    def pull_requests(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["PullRequest"]:
        queryset = PullRequestModel.objects.filter(repository=self)

        return Pagination[PullRequest](queryset=queryset, pagination=pagination)

    @gql.django.field
    def pull_request(
        self, id: Optional[strawberry.ID] = None, reference: Optional[str] = strawberry.UNSET
    ) -> "PullRequest":
        return (
            PullRequestModel.objects.get(id=id)
            if id is not None
            else PullRequestModel.objects.get(repository=self, reference=reference)
        )

    # Branches
    @gql.django.field
    def branches(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Branch"]:
        queryset = BranchModel.objects.filter(repository=self)

        return Pagination["Branch"](queryset=queryset, pagination=pagination)

    @gql.django.field
    def branch(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = strawberry.UNSET) -> "Branch":
        return (
            BranchModel.objects.get(id=id)
            if id is not None
            else BranchModel.objects.get(repository=self, reference=reference)
        )

    # Commits
    @gql.django.field
    def commits(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Commit"]:
        queryset = CommitModel.objects.filter(repository=self)

        return Pagination[Commit](queryset=queryset, pagination=pagination)

    @gql.django.field
    def commit(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = strawberry.UNSET) -> "Commit":
        return (
            CommitModel.objects.get(id=id)
            if id is not None
            else CommitModel.objects.get(repository=self, reference=reference)
        )


@gql.django.type(BranchModel)
class Branch:
    id: auto
    reference: auto
    repository: "Repository"

    # Pull Requests
    @gql.django.field
    def pull_requests(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["PullRequest"]:
        queryset = PullRequestModel.objects.filter(branch=self)

        return Pagination[PullRequest](queryset=queryset, pagination=pagination)

    # Commits
    @gql.django.field
    def commits(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Commit"]:
        queryset = CommitModel.objects.filter(branch=self)

        return Pagination[Commit](queryset=queryset, pagination=pagination)

    @gql.django.field
    def last_commit(self) -> Optional["Commit"]:
        return CommitModel.objects.filter(branch=self.id).order_by("-created_at").first()


@gql.django.type(PullRequestModel)
class PullRequest:
    id: auto
    reference: auto
    title: Optional[str]
    repository: "Repository"
    branch: "Branch"

    # Commits
    @gql.django.field
    def commits(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ) -> Pagination["Commit"]:
        queryset = CommitModel.objects.filter(pull_request=self)

        return Pagination[Commit](queryset=queryset, pagination=pagination)

    @gql.django.field
    def last_commit(self) -> Optional["Commit"]:
        return CommitModel.objects.filter(pull_request=self.id).order_by("-created_at").first()


@gql.django.type(CommitModel)
class Commit:
    id: auto
    reference: auto
    title: Optional[str]
    repository: "Repository"
    branch: "Branch"
    pull_request: Optional["PullRequest"]
    created_at: auto

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

        return Pagination[Run](queryset=queryset, apply_filters=apply_filters, order=order, pagination=pagination)

    @gql.django.field
    def last_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(commit=self.id).order_by("-created_at").first()

    @gql.django.field
    def last_successful_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(commit=self.id, status="success").order_by("-created_at").first()


@gql.django.type(AlertModel)
class Alert:
    id: auto
    name: auto
    channel: auto
    channel_metadata: JSON
    triggers: JSON
    is_active: auto
    created_at: auto
