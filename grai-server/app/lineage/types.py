import strawberry
import strawberry_django
from strawberry.scalars import JSON

from lineage.models import Edge as EdgeModel
from lineage.models import Filter as FilterModel
from lineage.models import Node as NodeModel
from users.types import User


@strawberry_django.filters.filter(NodeModel, lookups=True)
class NodeFilter:
    id: strawberry.auto
    namespace: strawberry.auto
    name: strawberry.auto
    display_name: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry_django.ordering.order(NodeModel)
class NodeOrder:
    id: strawberry.auto
    namespace: strawberry.auto
    name: strawberry.auto
    display_name: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry_django.filters.filter(EdgeModel, lookups=True)
class EdgeFilter:
    id: strawberry.auto
    namespace: strawberry.auto
    name: strawberry.auto
    display_name: strawberry.auto
    is_active: strawberry.auto
    source: NodeFilter
    destination: NodeFilter
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry_django.ordering.order(EdgeModel)
class EdgeOrder:
    id: strawberry.auto
    namespace: strawberry.auto
    name: strawberry.auto
    display_name: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry.django.type(FilterModel, pagination=True)
class Filter:
    id: strawberry.auto
    name: strawberry.auto
    metadata: JSON
    created_at: strawberry.auto
    updated_at: strawberry.auto
    created_by: User
