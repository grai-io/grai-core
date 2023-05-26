from typing import List

import strawberry_django
from strawberry.scalars import JSON
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from lineage.models import Edge as EdgeModel
from lineage.models import Filter as FilterModel
from lineage.models import Node as NodeModel
from users.types import User


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


@gql.django.type(FilterModel, pagination=True)
class Filter:
    id: auto
    name: auto
    metadata: JSON
    created_at: auto
    updated_at: auto
    created_by: User
