from typing import Optional

import strawberry
from asgiref.sync import sync_to_async
from strawberry.scalars import JSON
from strawberry.types import Info

from api.common import IsAuthenticated, aget_workspace, get_user

from .models import Filter as FilterModel
from .types import Filter


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createFilter(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        name: Optional[str],
        metadata: JSON,
    ) -> Filter:
        user = get_user(info)
        workspace = await aget_workspace(info, workspaceId)

        filter = await FilterModel.objects.acreate(
            workspace=workspace,
            name=name,
            metadata=metadata,
            created_by=user,
        )

        return filter

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateFilter(
        self,
        info: Info,
        id: strawberry.ID,
        name: Optional[str] = None,
        metadata: Optional[JSON] = None,
    ) -> Filter:
        user = get_user(info)

        try:
            filter = await FilterModel.objects.aget(pk=id, workspace__memberships__user_id=user.id)
        except FilterModel.DoesNotExist:
            raise Exception("Can't find filter")

        if name is not None:
            filter.name = name
        if metadata is not None:
            filter.metadata = metadata

        await sync_to_async(filter.save)()

        return filter

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def deleteFilter(
        self,
        id: strawberry.ID,
    ) -> Filter:
        filter = await FilterModel.objects.aget(id=id)

        await sync_to_async(filter.delete)()

        filter.id = id

        return filter
