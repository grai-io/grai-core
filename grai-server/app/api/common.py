import typing

from strawberry.permission import BasePermission
from strawberry.types import Info
from asgiref.sync import sync_to_async


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        if info.context.request.user is None:
            return False

        return sync_to_async(lambda: info.context.request.user.is_authenticated)


def get_user(info: Info):
    return info.context.request.user
