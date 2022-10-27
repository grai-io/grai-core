from typing import List

from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from api.mutations import Mutation
from api.types import EdgeType, NodeType, UserType


@gql.type
class Query:
    node: List[NodeType] = gql.django.field()
    edge: List[EdgeType] = gql.django.field()
    user: List[UserType] = gql.django.field()


schema = gql.Schema(
    Query,
    # Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
