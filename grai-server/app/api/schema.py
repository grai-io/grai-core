from api.mutations import Mutation
from api.queries import Query
from strawberry.schema.config import StrawberryConfig
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

schema = gql.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
    config=StrawberryConfig(auto_camel_case=False),
)
