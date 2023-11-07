import strawberry
from asgiref.sync import sync_to_async
from strawberry.types import Info

from api.common import IsAuthenticated, get_user, get_workspace
from api.pagination import DataWrapper

from .models import UserChat
from .types import Chat


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def fetchOrCreateChats(
        self,
        info: Info,
        workspaceId: strawberry.ID,
    ) -> DataWrapper[Chat]:
        def _fetch_or_create(
            info: Info,
            workspaceId: strawberry.ID,
        ) -> DataWrapper[Chat]:
            user = get_user(info)
            workspace = get_workspace(info, workspaceId)

            membership = workspace.memberships.get(user=user)

            chats = UserChat.objects.filter(membership=membership).all()

            if len(chats) == 0:
                chats = [UserChat.objects.create(membership=membership)]

            return DataWrapper(chats)

        return await sync_to_async(_fetch_or_create)(
            info,
            workspaceId,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def fetchOrCreateChat(
        self,
        info: Info,
        workspaceId: strawberry.ID,
    ) -> Chat:
        def _fetch_or_create(
            info: Info,
            workspaceId: strawberry.ID,
        ) -> DataWrapper[Chat]:
            user = get_user(info)
            workspace = get_workspace(info, workspaceId)

            membership = workspace.memberships.get(user=user)

            try:
                chat = UserChat.objects.filter(membership=membership).order_by("id").first()
            except UserChat.DoesNotExist:
                chat = UserChat.objects.create(membership=membership)

            return chat

        return await sync_to_async(_fetch_or_create)(
            info,
            workspaceId,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createChat(
        self,
        info: Info,
        workspaceId: strawberry.ID,
    ) -> Chat:
        def _create(
            info: Info,
            workspaceId: strawberry.ID,
        ) -> DataWrapper[Chat]:
            user = get_user(info)
            workspace = get_workspace(info, workspaceId)

            membership = workspace.memberships.get(user=user)

            return UserChat.objects.create(membership=membership)

        return await sync_to_async(_create)(
            info,
            workspaceId,
        )
