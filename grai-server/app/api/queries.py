import typing

from workspaces.utils import set_current_user

from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry_django_plus import gql
from asgiref.sync import sync_to_async

from api.types import Connector, User, Workspace

from .common import IsAuthenticated, get_user


class WorkspaceFilter(BasePermission):
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        if info.context.request.user is None:
            return False

        is_authenticated = await sync_to_async(lambda: info.context.request.user.is_authenticated)()

        if not is_authenticated:
            return False

        set_current_user(info.context.request.user)

        return True


def get_profile(info: Info) -> User:
    return get_user(info)


@gql.type
class Query:
    workspaces: typing.List[Workspace] = gql.django.field(permission_classes=[IsAuthenticated, WorkspaceFilter])
    workspace: Workspace = gql.django.field(permission_classes=[IsAuthenticated, WorkspaceFilter])
    connectors: typing.List[Connector] = gql.django.field(permission_classes=[IsAuthenticated])
    profile: User = gql.django.field(resolver=get_profile, permission_classes=[IsAuthenticated])
