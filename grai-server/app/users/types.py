from typing import Optional

import strawberry
import strawberry_django

from .models import User as UserModel


@strawberry_django.filters.filter(UserModel, lookups=True)
class UserFilter:
    username: strawberry.auto
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry_django.ordering.order(UserModel)
class UserOrder:
    username: strawberry.auto
    first_name: strawberry.auto
    last_name: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry.django.type(UserModel, order=UserOrder, filters=UserFilter)
class User:
    id: strawberry.auto
    username: strawberry.auto
    first_name: strawberry.auto
    last_name: strawberry.auto

    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    created_at: strawberry.auto
    updated_at: strawberry.auto
