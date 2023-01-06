import typing

from strawberry.permission import BasePermission
from strawberry.types import Info
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        if info.context.request.user and not info.context.request.user.is_anonymous:
            return True

        user, token = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        if user.is_authenticated:
            info.context.request.user = user

        return user.is_authenticated


def get_user(info: Info):
    return info.context.request.user
