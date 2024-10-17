from typing import Optional

import strawberry
from django.db.models.query import QuerySet
from strawberry.types.field import StrawberryField
from strawberry_django.ordering import process_order


def apply_order(queryset: QuerySet, order: Optional[StrawberryField] = strawberry.UNSET):
    if order:
        queryset, args = process_order(order, info=None, queryset=queryset)
    # queryset = queryset.order_by(*generate_order_args(order))

    return queryset
