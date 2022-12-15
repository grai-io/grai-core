from workspaces.models import Workspace, WorkspaceAPIKey
from api.types import EdgeType, NodeType, UserType, ConnectionType, KeyResultType
from lineage.models import Edge, Node
from connections.models import Connection
from strawberry_django_plus import gql
from strawberry.scalars import JSON
import strawberry
from strawberry.types import Info
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication


# @strawberry.django.input(Node)
# class NodeTypeInput:
#     name: gql.auto


# @gql.django.partial(Node)
# class NodeTypeInputPartial(gql.NodeInput):
#     display_name: gql.auto


@strawberry.django.input(Connection)
class ConnectionTypeInput:
    workspace: gql.auto
    connector: gql.auto
    namespace: gql.auto
    name: gql.auto
    metadata: gql.auto
    secrets: gql.auto


# @gql.django.partial(Connection)
# class ConnectionTypeInputPartial(gql.NodeInput):
#     namespace: gql.auto
#     name: gql.auto
#     metadata: gql.auto
#     secrets: gql.auto


@strawberry.type
class Mutation:
    # create_model: NodeType = gql.django.create_mutation(NodeTypeInput)
    # update_model: NodeType = strawberry.django.update_mutation(NodeTypeInputPartial)
    # delete_model: NodeType = gql.django.delete_mutation(gql.NodeInput)
    create_connection: ConnectionType = gql.django.create_mutation(ConnectionTypeInput)

    @strawberry.mutation
    async def update_connection(
        self,
        id: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: JSON,
    ) -> ConnectionType:
        connection = await sync_to_async(Connection.objects.get)(pk=id)

        mergedSecrets = dict()
        mergedSecrets.update(connection.secrets)
        mergedSecrets.update(secrets)

        connection.namespace = namespace
        connection.name = name
        connection.metadata = metadata
        connection.secrets = mergedSecrets
        await sync_to_async(connection.save)()

        return connection

    @strawberry.mutation
    async def create_api_key(
        self, info: Info, name: str, workspaceId: strawberry.ID
    ) -> KeyResultType:
        user, _ = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        workspace = await sync_to_async(Workspace.objects.get)(pk=workspaceId)

        api_key, key = await sync_to_async(WorkspaceAPIKey.objects.create_key)(
            name=name, created_by=user, workspace=workspace
        )

        return KeyResultType(key=key, api_key=api_key)
