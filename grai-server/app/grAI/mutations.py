import strawberry
from asgiref.sync import sync_to_async
from strawberry.types import Info

from api.common import IsAuthenticated, get_user, get_workspace
from api.pagination import DataWrapper

from .models import Message, MessageRoles, UserChat
from .types import Chat


@strawberry.type
class Mutation:
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
            def add_message(message: str):
                Message.objects.create(
                    chat=chat,
                    message=message,
                    visible=True,
                    role=MessageRoles.AGENT,
                )

            user = get_user(info)
            workspace = get_workspace(info, workspaceId)

            membership = workspace.memberships.get(user=user)

            chat = UserChat.objects.create(membership=membership)

            add_message("Chat restarted")
            add_message("Hello, I'm the GrAI assistant. How can I help you?")

            return chat

        return await sync_to_async(_create)(
            info,
            workspaceId,
        )
