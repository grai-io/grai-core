import strawberry

from api.pagination import Pagination

from .models import Message as MessageModel
from .models import UserChat as UserChatModel


@strawberry.django.type(MessageModel, pagination=True)
class Message:
    id: strawberry.auto
    message: strawberry.auto
    role: strawberry.auto
    created_at: strawberry.auto


@strawberry.django.type(UserChatModel, pagination=True)
class Chat:
    id: strawberry.auto

    # Messages
    @strawberry.django.field
    def messages(
        self,
    ) -> Pagination[Message]:
        queryset = MessageModel.objects.filter(chat=self)

        return Pagination[Message](queryset=queryset)
