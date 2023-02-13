from strawberry.schema.config import StrawberryConfig
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from api.mutations.base import Mutation
from api.queries import Query

schema = gql.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
    config=StrawberryConfig(auto_camel_case=False),
)
