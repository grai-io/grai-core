from typing import List, Optional

import strawberry_django
from strawberry.types import Info
from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from api.types import Connector, User, Workspace
from connections.models import Connector as ConnectorModel
from workspaces.models import Workspace as WorkspaceModel

from .common import IsAuthenticated, get_user


def get_workspaces(info: Info) -> List[Workspace]:
    user = get_user(info)

    return WorkspaceModel.objects.filter(memberships__user_id=user.id)


def get_workspace(
    info: Info,
    id: Optional[gql.ID] = None,
    name: Optional[str] = None,
    organisationName: Optional[str] = None,
) -> Workspace:
    user = get_user(info)

    try:
        query = {"id": id} if id else {"name": name, "organisation__name": organisationName}
        workspace = WorkspaceModel.objects.get(**query, memberships__user_id=user.id)
    except WorkspaceModel.DoesNotExist:
        raise Exception("Can't find workspace")

    return workspace


def get_profile(info: Info) -> User:
    return get_user(info)


@strawberry_django.ordering.order(ConnectorModel)
class ConnectorOrder:
    id: auto
    name: auto
    category: auto


@gql.type
class Query:
    workspaces: List[Workspace] = gql.django.field(resolver=get_workspaces, permission_classes=[IsAuthenticated])
    workspace: Workspace = gql.django.field(resolver=get_workspace, permission_classes=[IsAuthenticated])
    connectors: List[Connector] = gql.django.field(
        permission_classes=[IsAuthenticated], order=ConnectorOrder, pagination=True
    )
    profile: User = gql.django.field(resolver=get_profile, permission_classes=[IsAuthenticated])
