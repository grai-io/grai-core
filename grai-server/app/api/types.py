import datetime
from typing import List, Optional

import strawberry
import strawberry_django
from strawberry.scalars import JSON
from strawberry_django.filters import FilterLookup
from strawberry_django_plus.gql import auto

from connections.models import (
    Connection as ConnectionModel,
    Connector as ConnectorModel,
    Run as RunModel,
)
from lineage.models import Edge as EdgeModel, Node as NodeModel
from users.models import User as UserModel
from workspaces.models import (
    Membership as MembershipModel,
    Organisation as OrganisationModel,
    Workspace as WorkspaceModel,
    WorkspaceAPIKey as WorkspaceAPIKeyModel,
)


@strawberry.django.filters.filter(UserModel, lookups=True)
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


@strawberry.django.type(UserModel, order=UserOrder, filters=UserFilter)
class User:
    id: auto
    username: auto
    first_name: auto
    last_name: auto

    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    created_at: auto
    updated_at: auto


@strawberry.django.filters.filter(NodeModel, lookups=True)
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


@strawberry.django.type(NodeModel, order=NodeOrder, filters=NodeFilter, pagination=True)
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


@strawberry.django.filters.filter(EdgeModel, lookups=True)
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


@strawberry.django.type(EdgeModel, order=EdgeOrder, filters=EdgeFilter, pagination=True)
class Edge:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    source: Node
    destination: Node
    metadata: JSON
    is_active: auto
    created_at: auto
    updated_at: auto


@strawberry.django.filters.filter(ConnectorModel, lookups=True)
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


@strawberry.django.type(
    ConnectorModel, order=ConnectorOrder, filters=ConnectorFilter, pagination=True
)
class Connector:
    id: auto
    name: auto
    metadata: JSON
    is_active: auto
    icon: Optional[str]
    category: Optional[str]
    coming_soon: auto


@strawberry.django.filters.filter(ConnectionModel, lookups=True)
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


@strawberry.django.type(
    ConnectionModel, order=ConnectionOrder, filters=ConnectionFilter, pagination=True
)
class Connection:
    id: auto
    connector: Connector
    namespace: auto
    name: auto
    metadata: JSON
    schedules: JSON
    is_active: auto
    created_at: auto
    updated_at: auto
    created_by: User

    runs: List["Run"]
    # run: Run = strawberry.django.field
    @strawberry.django.field
    def run(self, id: strawberry.ID) -> "Run":
        return RunModel.objects.get(id=id)

    @strawberry.django.field
    def last_run(self) -> Optional["Run"]:
        return (
            RunModel.objects.filter(connection=self.id).order_by("-created_at").first()
        )

    @strawberry.django.field
    def last_successful_run(self) -> Optional["Run"]:
        return (
            RunModel.objects.filter(connection=self.id, status="success")
            .order_by("-created_at")
            .first()
        )


@strawberry.django.type(OrganisationModel)
class Organisation:
    id: auto
    name: auto


@strawberry.django.filters.filter(WorkspaceModel)
class WorkspaceFilter:
    id: auto
    name: FilterLookup[str]
    memberships: FilterLookup["MembershipFilter"]


@strawberry_django.ordering.order(WorkspaceModel)
class WorkspaceOrder:
    id: auto
    name: auto


@strawberry.django.type(
    WorkspaceModel, order=WorkspaceOrder, filters=WorkspaceFilter, pagination=True
)
class Workspace:
    id: auto
    name: auto
    organisation: Organisation
    nodes: List["Node"]
    # node: NodeType = strawberry.django.field
    @strawberry.django.field
    def node(self, id: strawberry.ID) -> Node:
        return NodeModel.objects.get(id=id)

    edges: List["Edge"]
    # edge: EdgeType = strawberry.django.field(field_name='edges')
    @strawberry.django.field
    def edge(self, id: strawberry.ID) -> Edge:
        return EdgeModel.objects.get(id=id)

    connections: List["Connection"]
    # connection: ConnectionType = strawberry.django.field
    @strawberry.django.field
    def connection(self, id: strawberry.ID) -> Connection:
        return ConnectionModel.objects.get(id=id)

    runs: List["Run"]
    # run: Run = strawberry.django.field
    @strawberry.django.field
    def run(self, id: strawberry.ID) -> "Run":
        return RunModel.objects.get(id=id)

    memberships: List["Membership"]
    api_keys: List["WorkspaceAPIKey"]


@strawberry.django.filters.filter(MembershipModel, lookups=True)
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


@strawberry.django.type(
    MembershipModel, order=MembershipOrder, filters=MembershipFilter, pagination=True
)
class Membership:
    id: auto
    role: auto
    user: User
    workspace: Workspace
    is_active: auto
    created_at: auto


@strawberry.django.filters.filter(WorkspaceAPIKeyModel, lookups=True)
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


@strawberry.django.type(
    WorkspaceAPIKeyModel,
    order=WorkspaceAPIKeyOrder,
    filters=WorkspaceAPIKeyFilter,
    pagination=True,
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


@strawberry.type
class KeyResult:
    key: str
    api_key: WorkspaceAPIKey


@strawberry.type
class BasicResult:
    success: bool


@strawberry_django.ordering.order(RunModel)
class RunOrder:
    id: auto
    created_at: auto


@strawberry.django.type(RunModel, order=RunOrder, pagination=True)
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
