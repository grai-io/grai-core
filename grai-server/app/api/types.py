from typing import List

from strawberry.scalars import JSON
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from lineage.models import Edge, Node
from users.models import User


@gql.django.type(User)
class UserType:
    id: auto
    username: auto

    created_at: auto
    updated_at: auto


@gql.django.type(Node)
class NodeType:
    id: auto
    namespace: auto
    name: auto
    display_name: auto
    data_source: auto
    metadata: JSON
    is_active: auto
    created_by: UserType
    source_edge: List["EdgeType"]
    destination_edge: List["EdgeType"]


@gql.django.type(Edge)
class EdgeType:
    id: auto
    data_source: auto
    source: NodeType
    destination: NodeType
    metadata: JSON
    is_active: auto
    created_by: UserType
