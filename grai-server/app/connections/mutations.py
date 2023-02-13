import uuid
from typing import Optional

import strawberry
from asgiref.sync import sync_to_async
from strawberry.file_uploads import Upload
from strawberry.scalars import JSON
from strawberry.types import Info

from api.common import IsAuthenticated, get_user, get_workspace
from api.types import Connection, Run
from connections.models import Connection as ConnectionModel
from connections.models import Connector as ConnectorModel
from connections.models import Run as RunModel
from connections.models import RunFile as RunFileModel
from connections.tasks import run_update_server


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createConnection(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        connectorId: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: Optional[JSON],
        schedules: Optional[JSON],
        is_active: Optional[bool],
    ) -> Connection:
        workspace = await get_workspace(info, workspaceId)

        connection = await ConnectionModel.objects.acreate(
            workspace=workspace,
            connector_id=connectorId,
            namespace=namespace,
            name=name,
            metadata=metadata,
            secrets=secrets,
            schedules=schedules,
            is_active=is_active if is_active is not None else True,
        )

        return connection

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateConnection(
        self,
        info: Info,
        id: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: Optional[JSON],
        schedules: Optional[JSON],
        is_active: Optional[bool],
    ) -> Connection:
        user = get_user(info)

        try:
            connection = await ConnectionModel.objects.aget(pk=id, workspace__memberships__user_id=user.id)
        except ConnectionModel.DoesNotExist:
            raise Exception("Can't find connection")

        mergedSecrets = dict()
        mergedSecrets.update(connection.secrets if connection.secrets else {})
        mergedSecrets.update(secrets if secrets else {})

        connection.namespace = namespace
        connection.name = name
        connection.metadata = metadata
        connection.secrets = mergedSecrets
        connection.schedules = schedules
        connection.is_active = is_active
        await sync_to_async(connection.save)()

        return connection

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def runConnection(
        self,
        info: Info,
        connectionId: strawberry.ID,
    ) -> Connection:
        user = get_user(info)

        try:
            connection = await sync_to_async(ConnectionModel.objects.get)(
                pk=connectionId, workspace__memberships__user_id=user.id
            )
        except ConnectionModel.DoesNotExist:
            raise Exception("Can't find connection")

        run = await sync_to_async(RunModel.objects.create)(
            connection=connection,
            workspace_id=connection.workspace_id,
            user=user,
            status="queued",
        )

        run_update_server.delay(run.id)

        return connection

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def uploadConnectorFile(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        namespace: str,
        connectorId: strawberry.ID,
        file: Upload,
    ) -> Run:
        user = get_user(info)
        workspace = await get_workspace(info, workspaceId)
        connector = await ConnectorModel.objects.aget(pk=connectorId)
        connection = await ConnectionModel.objects.acreate(
            connector=connector,
            workspace=workspace,
            name=f"{connector.name} {uuid.uuid4()}",
            temp=True,
            namespace=namespace,
        )
        run = await RunModel.objects.acreate(workspace=workspace, connection=connection, status="queued", user=user)
        runFile = RunFileModel(run=run)
        runFile.file = file
        await sync_to_async(runFile.save)()

        run_update_server.delay(run.id)

        return run
