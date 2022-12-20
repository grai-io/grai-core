import typing

import strawberry

# from api.mutations import Mutation
from api.types import EdgeType, NodeType, UserType
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        user, token = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        return user.is_authenticated


@gql.type
class Query:
    nodes: typing.List[NodeType] = strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
    node: NodeType = strawberry.django.field(permission_classes=[IsAuthenticated])
    edges: typing.List[EdgeType] = strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
    users: typing.List[UserType] = strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )


schema = gql.Schema(
    Query,
    # Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
