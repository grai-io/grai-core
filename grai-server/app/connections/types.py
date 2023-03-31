from typing import Optional

import strawberry_django
from strawberry.scalars import JSON
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from .models import Connector as ConnectorModel


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
