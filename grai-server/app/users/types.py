from typing import Optional

import strawberry_django
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from .models import User as UserModel


@gql.django.filters.filter(UserModel, lookups=True)
class UserFilter:
    username: auto
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: auto
    updated_at: auto


@strawberry_django.ordering.order(UserModel)
class UserOrder:
    username: auto
    first_name: auto
    last_name: auto
    created_at: auto
    updated_at: auto


@gql.django.type(UserModel, order=UserOrder, filters=UserFilter)
class User:
    id: auto
    username: auto
    first_name: auto
    last_name: auto

    @gql.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    created_at: auto
    updated_at: auto
