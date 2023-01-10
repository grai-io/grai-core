import typing

import strawberry
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
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
    profile: User = strawberry.django.field(
        resolver=get_profile, permission_classes=[IsAuthenticated]
    )
