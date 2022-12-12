from api.types import EdgeType, NodeType, UserType, ConnectionType
from lineage.models import Edge, Node
from connections.models import Connection
from strawberry_django_plus import gql
import strawberry


# @strawberry.django.input(Node)
# class NodeTypeInput:
#     name: gql.auto


# @gql.django.partial(Node)
# class NodeTypeInputPartial(gql.NodeInput):
#     display_name: gql.auto

@strawberry.django.input(Connection)
class ConnectionTypeInput:
    connector: gql.auto
    namespace: gql.auto
    name: gql.auto
    metadata: gql.auto
    secrets: gql.auto

@strawberry.type
class Mutation:
    # create_model: NodeType = gql.django.create_mutation(NodeTypeInput)
    # update_model: NodeType = strawberry.django.update_mutation(NodeTypeInputPartial)
    # delete_model: NodeType = gql.django.delete_mutation(gql.NodeInput)
    create_connection: ConnectionType = gql.django.create_mutation(ConnectionTypeInput)