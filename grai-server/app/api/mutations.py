from workspaces.models import Workspace as WorkspaceModel, WorkspaceAPIKey
from api.types import Connection, Connector, Workspace, KeyResult
from connections.models import Connection as ConnectionModel
from strawberry_django_plus import gql
from strawberry.scalars import JSON
import strawberry
from strawberry.types import Info
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_connection(
        self,
        workspaceId: strawberry.ID,
        connectorId: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: JSON,
    ) -> Connection:
        connection = await sync_to_async(ConnectionModel.objects.create)(
            workspace_id=workspaceId,
            connector_id=connectorId,
            namespace=namespace,
            name=name,
            metadata=metadata,
            secrets=secrets,
        )

        return connection

    @strawberry.mutation
    async def update_connection(
        self,
        id: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: JSON,
    ) -> Connection:
        connection = await sync_to_async(ConnectionModel.objects.get)(pk=id)

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
    ) -> KeyResult:
        user, _ = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        workspace = await sync_to_async(WorkspaceModel.objects.get)(pk=workspaceId)

        api_key, key = await sync_to_async(WorkspaceAPIKey.objects.create_key)(
            name=name, created_by=user, workspace=workspace
        )

        return KeyResult(key=key, api_key=api_key)
