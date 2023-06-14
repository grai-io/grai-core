from typing import Optional

import strawberry
from api.common import IsAuthenticated, get_workspace
from api.types import Alert
from asgiref.sync import sync_to_async
from notifications.models import Alert as AlertModel
from strawberry.scalars import JSON
from strawberry.types import Info


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createAlert(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        name: str,
        channel: str,
        channel_metadata: JSON,
        triggers: JSON,
        is_active: Optional[bool] = True,
    ) -> Alert:
        workspace = await get_workspace(info, workspaceId)

        alert = await AlertModel.objects.acreate(
            workspace=workspace,
            name=name,
            channel=channel,
            channel_metadata=channel_metadata,
            triggers=triggers,
            is_active=is_active,
        )

        return alert

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateAlert(
        self,
        id: strawberry.ID,
        name: Optional[str] = None,
        channel_metadata: Optional[JSON] = None,
        triggers: Optional[JSON] = None,
        is_active: Optional[bool] = None,
    ) -> Alert:
        alert = await AlertModel.objects.aget(id=id)

        if name is not None:
            alert.name = name

        if channel_metadata is not None:
            alert.channel_metadata = channel_metadata

        if triggers is not None:
            alert.triggers = triggers

        if is_active is not None:
            alert.is_active = is_active

        await sync_to_async(alert.save)()

        return alert

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def deleteAlert(
        self,
        id: strawberry.ID,
    ) -> Alert:
        alert = await AlertModel.objects.aget(id=id)

        await sync_to_async(alert.delete)()

        alert.id = id

        return alert
