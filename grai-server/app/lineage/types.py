from typing import List

import strawberry_django
from lineage.models import Edge as EdgeModel
from lineage.models import Filter as FilterModel
from lineage.models import Node as NodeModel
from strawberry.scalars import JSON
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto
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


@gql.django.type(FilterModel, pagination=True)
class Filter:
    id: auto
    name: auto
    metadata: JSON
    created_at: auto
    updated_at: auto
    created_by: User
