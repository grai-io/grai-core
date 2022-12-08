from typing import List

# from api.mutations import Mutation
from api.types import EdgeType, NodeType, UserType
import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


@gql.type
class Query:
    nodes: List[NodeType] = strawberry.django.field()
    node: NodeType = strawberry.django.field()
    edges: List[EdgeType] = strawberry.django.field()
    users: List[UserType] = strawberry.django.field()


schema = gql.Schema(
    Query,
    # Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
