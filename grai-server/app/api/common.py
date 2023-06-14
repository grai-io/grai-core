import typing

import strawberry
from asgiref.sync import sync_to_async
from strawberry.permission import BasePermission
from strawberry.types import Info

from workspaces.models import Workspace


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        if info.context.request.user is None:
            return False

        return await sync_to_async(lambda: info.context.request.user.is_authenticated)()


def get_user(info: Info):
    return info.context.request.user


async def get_workspace(info: Info, workspaceId: strawberry.ID):
    user = get_user(info)

    try:
        workspace = await Workspace.objects.aget(pk=workspaceId, memberships__user_id=user.id)
    except Workspace.DoesNotExist:
        raise Exception("Can't find workspace")

    return workspace
