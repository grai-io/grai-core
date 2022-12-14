import typing

from api.types import (
    ConnectorType,
    WorkspaceType,
)
import strawberry
from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry_django_plus import gql
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        user, token = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        return user.is_authenticated


@gql.type
class Query:
    workspaces: typing.List[WorkspaceType] = strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
    workspace: WorkspaceType = strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
    connectors: typing.List[ConnectorType] = strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
