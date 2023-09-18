from typing import Optional

import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from django_otp import devices_for_user

from api.pagination import DataWrapper

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


@strawberry.type
class Device:
    id: strawberry.ID
    name: str


@strawberry.django.type(UserModel, order=UserOrder, filters=UserFilter)
class Profile(User):
    @strawberry.field
    async def devices(self) -> DataWrapper[Device]:
        def fetch_devices(user) -> DataWrapper[Device]:
            return [Device(id=device.persistent_id, name=device.name) for device in devices_for_user(user)]

        devices = await sync_to_async(fetch_devices)(self)

        return DataWrapper(devices)
