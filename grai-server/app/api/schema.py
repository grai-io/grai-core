from typing import List

# from api.mutations import Mutation
from api.types import EdgeType, NodeType, UserType
from strawberry_django_plus import gql
import strawberry
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


@gql.type
class Query:
    node: List[NodeType] = strawberry.django.field()
    edge: List[EdgeType] = strawberry.django.field()
    user: List[UserType] = strawberry.django.field()


schema = gql.Schema(
    Query,
    # Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
