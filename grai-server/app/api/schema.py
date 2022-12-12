from api.queries import Query
from api.mutations import Mutation
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


schema = gql.Schema(
    Query,
    Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
