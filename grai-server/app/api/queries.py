import typing

import strawberry
from django_multitenant.utils import set_current_tenant
from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry_django_plus import gql

from api.types import Connector, User, Workspace
from workspaces.models import Workspace as WorkspaceModel

from .common import IsAuthenticated, get_user


def get_workspaces(info: Info) -> typing.List[Workspace]:
    user = get_user(info)

    return WorkspaceModel.objects.filter(memberships__user_id=user.id)


def get_workspace(pk: strawberry.ID, info: Info) -> Workspace:
    user = get_user(info)

    try:
        workspace = WorkspaceModel.objects.get(id=pk, memberships__user_id=user.id)
    except WorkspaceModel.DoesNotExist:
        raise Exception("Can't find workspace")

    return workspace


def get_profile(info: Info) -> User:
    return get_user(info)


class WorkspaceFilter(BasePermission):
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        set_current_tenant(source)
        return True


@gql.type
class Query:
    workspaces: typing.List[Workspace] = gql.django.field(resolver=get_workspaces, permission_classes=[IsAuthenticated])
    # workspace: Workspace = gql.django.field(
    #     resolver=get_workspace
    # )
    workspace: Workspace = gql.django.field(permission_classes=[IsAuthenticated, WorkspaceFilter])
    connectors: typing.List[Connector] = gql.django.field(permission_classes=[IsAuthenticated])
    profile: User = gql.django.field(resolver=get_profile, permission_classes=[IsAuthenticated])
