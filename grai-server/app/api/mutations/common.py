import strawberry
from strawberry.types import Info

from api.common import get_user
from workspaces.models import Workspace as WorkspaceModel


async def get_workspace(info: Info, workspaceId: strawberry.ID):
    user = get_user(info)

    try:
        workspace = await WorkspaceModel.objects.aget(pk=workspaceId, memberships__user_id=user.id)
    except WorkspaceModel.DoesNotExist:
        raise Exception("Can't find workspace")

    return workspace
