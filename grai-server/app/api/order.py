from typing import Optional

import strawberry
from django.db.models.query import QuerySet
from strawberry.field import StrawberryField
from strawberry_django.ordering import generate_order_args


def apply_order(queryset: QuerySet, order: Optional[StrawberryField] = strawberry.UNSET):
    if order:
        queryset = queryset.order_by(*generate_order_args(order))

    return queryset
