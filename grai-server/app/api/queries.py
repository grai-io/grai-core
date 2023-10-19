from typing import List, Optional

import strawberry
import strawberry_django
from strawberry.types import Info

from api.types import Connector, Workspace
from connections.models import Connector as ConnectorModel
from users.types import Profile
from workspaces.models import Workspace as WorkspaceModel

from .common import IsAuthenticated, get_user


def get_workspaces(info: Info) -> List[Workspace]:
    user = get_user(info)

    return WorkspaceModel.objects.filter(memberships__user_id=user.id)


def get_workspace(
    info: Info,
    id: Optional[strawberry.ID] = None,
    name: Optional[str] = None,
    organisationName: Optional[str] = None,
) -> Workspace:
    user = get_user(info)

    try:
        query = None

        if id:
            query = {"id": id}
        elif name and organisationName:
            query = {"name": name, "organisation__name": organisationName}

        if not query:
            raise Exception("Can't find workspace")

        workspace = WorkspaceModel.objects.get(**query, memberships__user_id=user.id)
    except WorkspaceModel.DoesNotExist:
        raise Exception("Can't find workspace")

    return workspace


def get_profile(info: Info) -> Profile:
    return get_user(info)


# async def get_devices(info: Info) -> DataWrapper[Device]:
#     def fetch_devices(info: Info) -> DataWrapper[Device]:
#         user = get_user(info)
#         return [
#             Device(id=device.id, name=device.name) for device in devices_for_user(user)
#         ]

#     devices = await sync_to_async(fetch_devices)(info)

#     return DataWrapper(devices)


@strawberry_django.ordering.order(ConnectorModel)
class ConnectorOrder:
    id: strawberry.auto
    name: strawberry.auto
    category: strawberry.auto


@strawberry.type
class Query:
    workspaces: List[Workspace] = strawberry.django.field(resolver=get_workspaces, permission_classes=[IsAuthenticated])
    workspace: Workspace = strawberry.django.field(resolver=get_workspace, permission_classes=[IsAuthenticated])
    connectors: List[Connector] = strawberry.django.field(
        permission_classes=[IsAuthenticated], order=ConnectorOrder, pagination=True
    )
    profile: Profile = strawberry.django.field(resolver=get_profile, permission_classes=[IsAuthenticated])
    # devices: DataWrapper[Device] = strawberry.field(
    #     resolver=get_devices, permission_classes=[IsAuthenticated]
    # )
