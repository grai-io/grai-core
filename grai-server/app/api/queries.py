import typing

import strawberry
from strawberry.types import Info
from strawberry.scalars import JSON
from strawberry_django_plus import gql

from api.types import Connector, User, Workspace
from workspaces.models import Workspace as WorkspaceModel
from lineage.models import Node as NodeModel

from .common import IsAuthenticated, get_user


def get_workspaces(info: Info) -> typing.List[Workspace]:
    user = get_user(info)

    print(user.id)

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


def data_diff(
    info: Info,
    # workspaceId: strawberry.ID,
    # table1Id: strawberry.ID,
    # table2Id: strawberry.ID,
) -> JSON:
    import logging

    logging.basicConfig(level=logging.INFO)

    from data_diff import connect_to_table, diff_tables

    # table1Model = NodeModel.objects.get(pk=table1Id)
    # table2Model = NodeModel.objects.get(pk=table2Id)

    table1 = connect_to_table(
        "postgresql://grai:grai@localhost:5432/grai", "public.lineage_node", "id"
    )
    table2 = connect_to_table(
        "postgresql://grai:grai@localhost:5432/grai",
        "public.lineage_edge",
        "id",
    )

    return dict(diff_tables(table1, table2))


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
    data_diff: JSON = strawberry.django.field(
        resolver=data_diff, permission_classes=[IsAuthenticated]
    )
