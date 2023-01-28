import typing

from asgiref.sync import sync_to_async
from strawberry.permission import BasePermission
from strawberry.types import Info

from workspaces.utils import set_current_user


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        if info.context.request.user is None:
            return False

        return await sync_to_async(lambda: info.context.request.user.is_authenticated)()


class WorkspaceFilter(IsAuthenticated):
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        is_authenticated = await super().has_permission(source, info, **kwargs)

        if not is_authenticated:
            return False

        set_current_user(info.context.request.user)

        return True


def get_user(info: Info):
    return info.context.request.user
