import datetime
import time
from typing import List, Optional

import strawberry
import strawberry_django
from django.conf import settings
from django.db.models import Prefetch, Q
from strawberry.scalars import JSON
from strawberry_django.filters import FilterLookup
from strawberry_django.pagination import OffsetPaginationInput
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from api.search import Search
from connections.models import Connection as ConnectionModel
from connections.models import Connector as ConnectorModel
from connections.models import Run as RunModel
from installations.models import Branch as BranchModel
from installations.models import Commit as CommitModel
from installations.models import PullRequest as PullRequestModel
from installations.models import Repository as RepositoryModel
from lineage.models import Edge as EdgeModel
from lineage.models import Node as NodeModel
from users.models import User as UserModel
from workspaces.models import Membership as MembershipModel
from workspaces.models import Organisation as OrganisationModel
from workspaces.models import Workspace as WorkspaceModel
from workspaces.models import WorkspaceAPIKey as WorkspaceAPIKeyModel


@gql.django.filters.filter(UserModel, lookups=True)
class UserFilter:
    username: auto
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: auto
    updated_at: auto


@strawberry_django.ordering.order(UserModel)
class UserOrder:
    username: auto
    first_name: auto
    last_name: auto
    created_at: auto
    updated_at: auto


@gql.django.type(UserModel, order=UserOrder, filters=UserFilter)
class User:
    id: auto
    username: auto
    first_name: auto
    last_name: auto

    @gql.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    created_at: auto
    updated_at: auto


@gql.django.filters.filter(NodeModel, lookups=True)
class NodeFilter:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    is_active: auto
    created_at: auto
    updated_at: auto
    source_edges: "EdgeFilter"
    destination_edges: "EdgeFilter"


@strawberry_django.ordering.order(NodeModel)
class NodeOrder:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    is_active: auto
    created_at: auto
    updated_at: auto


@gql.django.type(NodeModel, order=NodeOrder, filters=NodeFilter, pagination=True, only=["id"])
class Node:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    metadata: JSON
    is_active: auto
    source_edges: List["Edge"]
    destination_edges: List["Edge"]


@gql.django.filters.filter(EdgeModel, lookups=True)
class EdgeFilter:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    is_active: auto
    source: NodeFilter
    destination: NodeFilter
    created_at: auto
    updated_at: auto


@strawberry_django.ordering.order(EdgeModel)
class EdgeOrder:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    is_active: auto
    created_at: auto
    updated_at: auto


@gql.django.type(EdgeModel, order=EdgeOrder, filters=EdgeFilter, pagination=True)
class Edge:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    source: Node = gql.django.field()
    destination: Node = gql.django.field()
    metadata: JSON
    is_active: auto
    created_at: auto
    updated_at: auto


@gql.django.filters.filter(ConnectorModel, lookups=True)
class ConnectorFilter:
    id: auto
    name: auto
    is_active: auto


@strawberry_django.ordering.order(ConnectorModel)
class ConnectorOrder:
    id: auto
    name: auto
    is_active: auto
    category: auto
    coming_soon: auto


@gql.django.type(ConnectorModel, order=ConnectorOrder, filters=ConnectorFilter, pagination=True)
class Connector:
    id: auto
    name: auto
    metadata: JSON
    is_active: auto
    icon: Optional[str]
    category: Optional[str]
    coming_soon: auto


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

    runs: List["Run"]

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
    def requirements_edges(self) -> List[Edge]:
        return EdgeModel.objects.filter(destination=self).filter(metadata__grai__edge_type="ColumnToColumn")


@gql.django.type(NodeModel, order=NodeOrder, filters=NodeFilter, pagination=True)
class Table(Node):
    @gql.django.field(
        prefetch_related=Prefetch(
            "source_edges",
            queryset=EdgeModel.objects.filter(metadata__grai__edge_type="TableToColumn").select_related("destination"),
            to_attr="edges_list",
        )
    )
    def columns(self) -> List[Column]:
        return list(set([edge.destination for edge in self.edges_list]))

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
    def source_tables(self) -> List["Table"]:
        tables = []

        for source in self.sources_list:
            tables.append(source.destination)

        for column in self.columns:
            for source in column.destination.sources_list:
                for table in source.destination.tables:
                    tables.append(table.source)

        return list(set(tables))

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
    def destination_tables(self) -> List["Table"]:
        tables = []

        for destination in self.destinations_list:
            tables.append(destination.source)

        for column in self.columns2:
            for destination in column.destination.destination_list:
                for table in destination.source.tables:
                    tables.append(table.source)

        return list(set(tables))


@gql.django.type(OrganisationModel)
class Organisation:
    id: auto
    name: auto


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
    def nodes(self) -> List["Node"]:
        return NodeModel.objects.filter(workspace=self)

    @gql.django.field
    def node(self, id: strawberry.ID) -> Node:
        return NodeModel.objects.get(id=id)

    # Edges
    @gql.django.field
    def edges(self) -> List["Edge"]:
        return EdgeModel.objects.filter(workspace=self)

    @gql.django.field
    def edge(self, id: strawberry.ID) -> Edge:
        return EdgeModel.objects.get(id=id)

    # Connections
    @gql.django.field
    def connections(self) -> List["Connection"]:
        return ConnectionModel.objects.filter(workspace=self, temp=False)

    @gql.django.field
    def connection(self, id: strawberry.ID) -> Connection:
        return ConnectionModel.objects.get(id=id)

    # Runs
    @gql.django.field
    def runs(
        self,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        action: Optional[str] = None,
    ) -> List["Run"]:
        q_filter = Q(workspace=self)

        if owner:
            q_filter &= Q(commit__repository__owner=owner, commit__repository__repo=repo)

        if branch:
            q_filter &= Q(commit__branch__reference=branch)

        if action:
            q_filter &= Q(action=action)

        return RunModel.objects.order_by("-created_at").filter(q_filter)

    @gql.django.field
    def run(self, id: strawberry.ID) -> "Run":
        return RunModel.objects.get(id=id)

    # Memberships
    @gql.django.field
    def memberships(self) -> List["Membership"]:
        return MembershipModel.objects.filter(workspace=self)

    # Api Keys
    api_keys: List["WorkspaceAPIKey"] = gql.django.field()

    # Tables
    @gql.django.field
    def tables(self, pagination: Optional[OffsetPaginationInput] = None) -> List[Table]:
        query_set = NodeModel.objects.filter(workspace_id=self.id, metadata__grai__node_type="Table")

        if pagination:
            start = pagination.offset
            stop = start + pagination.limit
            return query_set[start:stop]

        return query_set

    @gql.django.field
    def tables_count(self) -> int:
        return NodeModel.objects.filter(workspace_id=self.id, metadata__grai__node_type="Table").count()

    @gql.django.field
    def table(self, id: strawberry.ID) -> Table:
        return NodeModel.objects.filter(id=id, workspace_id=self.id, metadata__grai__node_type="Table")

    # Other edges
    @gql.django.field
    def other_edges(self) -> List[Edge]:
        return EdgeModel.objects.filter(workspace_id=self.id).exclude(
            metadata__has_key="grai.edge_type", metadata__grai__edge_type="TableToColumn"
        )

    @gql.django.field
    def other_edges_count(self) -> int:
        return (
            EdgeModel.objects.filter(workspace_id=self.id)
            .exclude(metadata__has_key="grai.edge_type", metadata__grai__edge_type="TableToColumn")
            .count()
        )

    # Repositories
    @gql.django.field
    def repositories(
        self, type: Optional[str] = None, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List["Repository"]:
        q_filter = Q(workspace=self)

        if type:
            q_filter &= Q(type=type)

        if owner:
            q_filter &= Q(owner=owner)

        if repo:
            q_filter &= Q(repo=repo)

        return RepositoryModel.objects.filter(q_filter)

    @gql.django.field
    def repository(
        self,
        id: Optional[strawberry.ID] = None,
        type: Optional[str] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> "Repository":
        return (
            RepositoryModel.objects.get(id=id)
            if id is not None
            else RepositoryModel.objects.get(workspace=self, type=type, owner=owner, repo=repo)
        )

    # Branches
    @gql.django.field
    def branches(self) -> List["Branch"]:
        return BranchModel.objects.filter(workspace=self)

    @gql.django.field
    def branch(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = None) -> "Branch":
        return (
            BranchModel.objects.get(id=id)
            if id is not None
            else BranchModel.objects.get(workspace=self, reference=reference)
        )

    # Pull Requests
    @gql.django.field
    def pull_requests(self) -> List["PullRequest"]:
        return PullRequestModel.objects.filter(workspace=self)

    @gql.django.field
    def pull_request(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = None) -> "PullRequest":
        return (
            PullRequestModel.objects.get(id=id)
            if id is not None
            else PullRequestModel.objects.get(workspace=self, reference=reference)
        )

    # Commits
    @gql.django.field
    def commits(self) -> List["Commit"]:
        return CommitModel.objects.filter(workspace=self)

    @gql.django.field
    def commit(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = None) -> "Commit":
        return (
            CommitModel.objects.get(id=id)
            if id is not None
            else CommitModel.objects.get(workspace=self, reference=reference)
        )

    # Algolia search key
    @gql.django.field
    def search_key(self) -> str:
        client = Search()

        valid_until = int(time.time()) + 3600

        return client.generate_secured_api_key(
            settings.ALGOLIA_SEARCH_KEY,
            {"filters": f"workspace_id:{str(self.id)}", "validUntil": valid_until, "restrictIndices": "main"},
        )


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


@strawberry_django.ordering.order(RunModel)
class RunOrder:
    id: auto
    created_at: auto


@gql.django.type(RunModel, order=RunOrder, pagination=True)
class Run:
    id: auto
    connection: Connection
    status: auto
    metadata: JSON
    created_at: auto
    updated_at: auto
    started_at: Optional[datetime.datetime]
    finished_at: Optional[datetime.datetime]
    user: Optional[User]
    commit: Optional["Commit"]


@gql.django.type(RepositoryModel)
class Repository:
    id: auto
    workspace: Workspace
    type: auto
    owner: auto
    repo: auto

    # Pull Requests
    pull_requests: List["PullRequest"]

    @gql.django.field
    def pull_request(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = None) -> "PullRequest":
        return (
            PullRequestModel.objects.get(id=id)
            if id is not None
            else PullRequestModel.objects.get(repository=self, reference=reference)
        )

    # Branches
    branches: List["Branch"]

    @gql.django.field
    def branch(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = None) -> "Branch":
        return (
            BranchModel.objects.get(id=id)
            if id is not None
            else BranchModel.objects.get(repository=self, reference=reference)
        )

    # Commits
    commits: List["Commit"]

    @gql.django.field
    def commit(self, id: Optional[strawberry.ID] = None, reference: Optional[str] = None) -> "Commit":
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

    pull_requests: List["PullRequest"]
    commits: List["Commit"]

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

    commits: List["Commit"]

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

    runs: List[Run]

    @gql.django.field
    def last_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(commit=self.id).order_by("-created_at").first()

    @gql.django.field
    def last_successful_run(self) -> Optional["Run"]:
        return RunModel.objects.filter(commit=self.id, status="success").order_by("-created_at").first()
