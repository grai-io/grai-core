from typing import List

from lineage.models import Edge, Node
from connections.models import Connection, Connector
from namespaces.models import Namespace
from workspaces.models import Workspace, Membership
import strawberry
from strawberry.scalars import JSON
from strawberry_django_plus.gql import auto
from users.models import User


@strawberry.django.type(User)
class UserType:
    id: auto
    username: auto

    created_at: auto
    updated_at: auto


@strawberry.django.type(Node)
class NodeType:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    metadata: JSON
    is_active: auto
    created_by: UserType
    source_edges: List["EdgeType"]
    destination_edges: List["EdgeType"]


@strawberry.django.type(Edge)
class EdgeType:
    id: auto
    data_source: auto
    source: NodeType
    destination: NodeType
    metadata: JSON
    is_active: auto
    created_by: UserType


@strawberry.django.type(Connector)
class ConnectorType:
    id: auto
    name: auto
    metadata: JSON
    is_active: auto


@strawberry.django.type(Connection)
class ConnectionType:
    id: auto
    connector: ConnectorType
    namespace: auto
    name: auto
    metadata: JSON
    is_active: auto
    created_at: auto
    updated_at: auto
    created_by: UserType


@strawberry.django.type(Namespace)
class NamespaceType:
    id: auto
    name: auto


@strawberry.django.type(Workspace)
class WorkspaceType:
    id: auto
    name: auto
    nodes: List["NodeType"]
    # node: NodeType = strawberry.django.field
    @strawberry.django.field
    def node(self, info, pk: strawberry.ID) -> NodeType:
        return Node.objects.filter(id=pk).first()
    
    edges: List["EdgeType"]
    # edge: EdgeType = strawberry.django.field(field_name='edges')
    @strawberry.django.field
    def edge(self, info, pk: strawberry.ID) -> EdgeType:
        return Edge.objects.filter(id=pk).first()

    connections: List["ConnectionType"]
    # connection: ConnectionType = strawberry.django.field
    @strawberry.django.field
    def connection(self, info, pk: strawberry.ID) -> ConnectionType:
        return Connection.objects.filter(id=pk).first()

    namespaces: List["NamespaceType"]
    # namespace: NamespaceType = strawberry.django.field
    @strawberry.django.field
    def namespace(self, info, pk: strawberry.ID) -> NamespaceType:
        return Namespace.objects.filter(id=pk).first()

    memberships: List["MembershipType"]


@strawberry.django.type(Membership)
class MembershipType:
    id: auto
    role: auto
    user: UserType
    workspace: WorkspaceType
