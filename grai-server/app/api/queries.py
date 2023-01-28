import typing

from strawberry.types import Info
from strawberry_django_plus import gql

from api.types import Connector, User, Workspace

from .common import IsAuthenticated, WorkspaceFilter, get_user


def get_profile(info: Info) -> User:
    return get_user(info)


@gql.type
class Query:
    workspaces: typing.List[Workspace] = gql.django.field(permission_classes=[WorkspaceFilter])
    workspace: Workspace = gql.django.field(permission_classes=[WorkspaceFilter])
    connectors: typing.List[Connector] = gql.django.field(permission_classes=[IsAuthenticated])
    profile: User = gql.django.field(resolver=get_profile, permission_classes=[IsAuthenticated])
