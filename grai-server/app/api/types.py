from typing import List

import strawberry
from lineage.models import Edge, Node
from strawberry.scalars import JSON
from strawberry_django_plus import gql
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
