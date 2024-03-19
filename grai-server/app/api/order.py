from typing import Optional

import strawberry
from django.db.models.query import QuerySet
from strawberry.field import StrawberryField
from strawberry_django.ordering import process_order


def apply_order(queryset: QuerySet, order: Optional[StrawberryField] = strawberry.UNSET):
    if order:
        queryset = queryset.order_by(*process_order(order))

    return queryset
