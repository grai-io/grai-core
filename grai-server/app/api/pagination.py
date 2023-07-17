from typing import Callable, Generic, List, Optional, TypeVar

import strawberry
from django.db.models.query import QuerySet
from strawberry.field import StrawberryField
from strawberry_django.pagination import OffsetPaginationInput

from .order import apply_order


@strawberry.type
class PaginationResult:
    total: int
    filtered: int
    limit: int
    offset: int


T = TypeVar("T")


@strawberry.type
class Pagination(Generic[T]):
    def __init__(
        self,
        queryset: QuerySet,
        filteredQueryset: Optional[QuerySet] = None,
        apply_filters: Callable[[QuerySet], QuerySet] = None,
        order: Optional[StrawberryField] = strawberry.UNSET,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET,
    ):
        self.queryset = queryset
        self.filteredQueryset = filteredQueryset
        self.apply_filters = apply_filters
        self.order = order
        self.pagination = pagination

    @strawberry.field
    async def meta(self) -> PaginationResult:
        total = await self.queryset.acount()

        return PaginationResult(
            total=total,
            filtered=await self.apply_filters(self.queryset).acount() if self.apply_filters else total,
            limit=self.pagination.limit if self.pagination else None,
            offset=self.pagination.offset if self.pagination else None,
        )

    @strawberry.django.field
    def data(self) -> List[T]:
        queryset = self.filteredQueryset if self.filteredQueryset is not None else self.queryset
        if self.filteredQueryset is None and self.apply_filters:
            queryset = self.apply_filters(queryset)
        queryset = apply_order(queryset, self.order)
        queryset = apply_pagination(queryset, self.pagination)

        return queryset


def apply_pagination(queryset: QuerySet, pagination: Optional[OffsetPaginationInput] = strawberry.UNSET):
    if pagination:
        start = pagination.offset
        stop = start + pagination.limit
        return queryset[start:stop]

    return queryset


@strawberry.type
class DataWrapper(Generic[T]):
    def __init__(self, data: List[T]):
        self.data = data

    @strawberry.django.field
    def data(self) -> List[T]:
        return self.data
