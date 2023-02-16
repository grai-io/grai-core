from strawberry.schema.config import StrawberryConfig
from strawberry.tools import merge_types
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from api.queries import Query
from auth.mutations import Mutation as AuthMutation
from connections.mutations import Mutation as ConnectionMutation
from installations.mutations import Mutation as InstallationMutation
from workspaces.mutations import Mutation as WorkspaceMutation

mutations = (AuthMutation, InstallationMutation, WorkspaceMutation, ConnectionMutation)
Mutation = merge_types("Mutation", mutations)

schema = gql.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
    config=StrawberryConfig(auto_camel_case=False),
)
