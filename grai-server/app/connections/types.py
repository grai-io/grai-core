from typing import Optional

import strawberry
import strawberry_django
from strawberry.scalars import JSON

from .models import Connector as ConnectorModel


@strawberry_django.filters.filter(ConnectorModel, lookups=True)
class ConnectorFilter:
    id: strawberry.auto
    name: strawberry.auto
    is_active: strawberry.auto


@strawberry_django.ordering.order(ConnectorModel)
class ConnectorOrder:
    id: strawberry.auto
    name: strawberry.auto
    is_active: strawberry.auto
    category: strawberry.auto
    events: strawberry.auto
    coming_soon: strawberry.auto


@strawberry.django.type(ConnectorModel, order=ConnectorOrder, filters=ConnectorFilter, pagination=True)
class Connector:
    id: strawberry.auto
    name: strawberry.auto
    slug: strawberry.auto
    metadata: JSON
    is_active: strawberry.auto
    icon: Optional[str]
    category: Optional[str]
    events: strawberry.auto
    coming_soon: strawberry.auto
