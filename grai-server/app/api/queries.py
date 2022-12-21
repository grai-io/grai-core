import typing


from api.types import Connector, Workspace
import strawberry
from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry_django_plus import gql
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async
from workspaces.models import Workspace as WorkspaceModel


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        user, token = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        return user.is_authenticated


def get_workspaces(info: Info) -> typing.List[Workspace]:
    user, token = JWTAuthentication().authenticate(request=info.context.request)

    return WorkspaceModel.objects.filter(memberships__user_id=user.id)


def get_workspace(pk: strawberry.ID, info: Info) -> Workspace:
    user, token = JWTAuthentication().authenticate(request=info.context.request)

    try:
        workspace = WorkspaceModel.objects.get(id=pk, memberships__user_id=user.id)
    except WorkspaceModel.DoesNotExist:
        raise Exception("Can't find workspace")

    return workspace


@gql.type
class Query:
    workspaces: typing.List[Workspace] = strawberry.django.field(
        resolver=get_workspaces, permission_classes=[IsAuthenticated]
    )
    workspace: Workspace = strawberry.django.field(
        resolver=get_workspace, permission_classes=[IsAuthenticated]
    )
    connectors: typing.List[Connector] = strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
