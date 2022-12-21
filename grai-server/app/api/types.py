from typing import List
from lineage.models import Edge as EdgeModel, Node as NodeModel
from connections.models import (
    Connection as ConnectionModel,
    Connector as ConnectorModel,
)
from workspaces.models import (
    Workspace as WorkspaceModel,
    Membership as MembershipModel,
    WorkspaceAPIKey as WorkspaceAPIKeyModel,
)
import strawberry
from lineage.models import Edge, Node
from strawberry.scalars import JSON
from strawberry_django_plus.gql import auto
from users.models import User as UserModel


@strawberry.django.type(UserModel)
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


@strawberry.django.type(NodeModel)
class Node:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    metadata: JSON
    is_active: auto
    created_by: User
    source_edges: List["Edge"]
    destination_edges: List["Edge"]


@strawberry.django.type(EdgeModel)
class Edge:
    id: auto
    data_source: auto
    source: Node
    destination: Node
    metadata: JSON
    is_active: auto
    created_by: User


@strawberry.django.type(ConnectorModel)
class Connector:
    id: auto
    name: auto
    metadata: JSON
    is_active: auto


@strawberry.django.type(ConnectionModel)
class Connection:
    id: auto
    connector: Connector
    namespace: auto
    name: auto
    metadata: JSON
    is_active: auto
    created_at: auto
    updated_at: auto
    created_by: User


@strawberry.django.type(WorkspaceModel)
class Workspace:
    id: auto
    name: auto
    nodes: List["Node"]
    # node: NodeType = strawberry.django.field
    @strawberry.django.field
    def node(self, pk: strawberry.ID) -> Node:
        return NodeModel.objects.get(id=pk)

    edges: List["Edge"]
    # edge: EdgeType = strawberry.django.field(field_name='edges')
    @strawberry.django.field
    def edge(self, pk: strawberry.ID) -> Edge:
        return EdgeModel.objects.get(id=pk)

    connections: List["Connection"]
    # connection: ConnectionType = strawberry.django.field
    @strawberry.django.field
    def connection(self, pk: strawberry.ID) -> Connection:
        return ConnectionModel.objects.get(id=pk)

    memberships: List["Membership"]
    api_keys: List["WorkspaceAPIKey"]


@strawberry.django.type(MembershipModel)
class Membership:
    id: auto
    role: auto
    user: User
    workspace: Workspace
    created_at: auto


@strawberry.django.type(WorkspaceAPIKeyModel)
class WorkspaceAPIKey:
    id: auto
    name: auto
    prefix: auto
    revoked: auto
    expiry_date: auto
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
