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
from workspaces.models import Workspace


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        user, token = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        return user.is_authenticated


def get_workspaces(info: Info) -> typing.List[WorkspaceType]:
    user, token = JWTAuthentication().authenticate(request=info.context.request)

    return [
        WorkspaceType(id=workspace.id, name=workspace.name)
        for workspace in Workspace.objects.filter(memberships__user_id=user.id)
    ]


def get_workspace(pk: strawberry.ID, info: Info) -> WorkspaceType:
    user, token = JWTAuthentication().authenticate(request=info.context.request)

    try:
        workspace = Workspace.objects.get(id=pk, memberships__user_id=user.id)
    except Workspace.DoesNotExist:
        raise Exception("Can't find workspace")

    return WorkspaceType(
        id=workspace.id,
        name=workspace.name,
        nodes=workspace.nodes,
        edges=workspace.edges,
        connections=workspace.connections,
    )


@gql.type
class Query:
    workspaces: typing.List[WorkspaceType] = strawberry.django.field(
        resolver=get_workspaces, permission_classes=[IsAuthenticated]
    )
    workspace: WorkspaceType = strawberry.django.field(
        resolver=get_workspace, permission_classes=[IsAuthenticated]
    )
    connectors: typing.List[ConnectorType] = strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
