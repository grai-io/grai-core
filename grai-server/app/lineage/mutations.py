from typing import Optional

import strawberry
from asgiref.sync import sync_to_async
from strawberry.scalars import JSON
from strawberry.types import Info

from api.common import IsAuthenticated, get_user, get_workspace

from .models import Filter as FilterModel, Source as SourceModel
from .types import Filter
from api.types import Source


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
        workspace = await get_workspace(info, workspaceId)

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

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createSource(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        name: str,
    ) -> Source:
        user = get_user(info)
        workspace = await get_workspace(info, workspaceId)

        source = await SourceModel.objects.acreate(
            workspace=workspace,
            name=name,
        )

        return source

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateSource(
        self,
        info: Info,
        id: strawberry.ID,
        name: Optional[str] = None,
    ) -> Source:
        user = get_user(info)

        try:
            source = await SourceModel.objects.aget(pk=id, workspace__memberships__user_id=user.id)
        except SourceModel.DoesNotExist:
            raise Exception("Can't find source")

        if name is not None:
            source.name = name

        await sync_to_async(source.save)()

        return source

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def deleteSource(
        self,
        id: strawberry.ID,
    ) -> Source:
        source = await SourceModel.objects.aget(id=id)

        await sync_to_async(source.delete)()

        source.id = id

        return source
