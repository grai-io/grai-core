import uuid
from typing import Optional

import strawberry
from asgiref.sync import sync_to_async
from strawberry.file_uploads import Upload
from strawberry.scalars import JSON
from strawberry.types import Info

from api.common import IsAuthenticated, aget_workspace, get_user, get_workspace
from api.types import Connection, Run, RunAction
from connections.models import Connection as ConnectionModel
from connections.models import Connector as ConnectorModel
from connections.models import Run as RunModel
from connections.models import RunFile as RunFileModel
from connections.tasks import process_run


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
        secrets: Optional[JSON] = None,
        schedules: Optional[JSON] = None,
        is_active: bool = True,
        temp: bool = False,
    ) -> Connection:
        workspace = await aget_workspace(info, workspaceId)

        connection = await ConnectionModel.objects.acreate(
            workspace=workspace,
            connector_id=connectorId,
            namespace=namespace,
            name=name,
            metadata=metadata,
            secrets=secrets,
            schedules=schedules,
            is_active=is_active,
            temp=temp,
        )

        return connection

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateConnection(
        self,
        info: Info,
        id: strawberry.ID,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[JSON] = None,
        secrets: Optional[JSON] = None,
        schedules: Optional[JSON] = None,
        is_active: Optional[bool] = None,
        temp: Optional[bool] = None,
    ) -> Connection:
        user = get_user(info)

        try:
            connection = await ConnectionModel.objects.aget(pk=id, workspace__memberships__user_id=user.id)
        except ConnectionModel.DoesNotExist:
            raise Exception("Can't find connection")

        if namespace is not None:
            connection.namespace = namespace
        if name is not None:
            connection.name = name
        if metadata is not None:
            connection.metadata = metadata
        if secrets is not None:
            mergedSecrets = dict()
            mergedSecrets.update(connection.secrets if connection.secrets else {})
            mergedSecrets.update(secrets if secrets else {})
            connection.secrets = mergedSecrets
        if schedules is not None:
            connection.schedules = schedules
        if is_active is not None:
            connection.is_active = is_active
        if temp is not None:
            connection.temp = temp
        await sync_to_async(connection.save)()

        return connection

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def runConnection(
        self,
        info: Info,
        connectionId: strawberry.ID,
        action: RunAction = RunModel.UPDATE,
    ) -> Run:
        def _run_connection(info: Info, connectionId: str, action: RunAction) -> Run:
            user = get_user(info)

            try:
                connection = ConnectionModel.objects.get(pk=connectionId, workspace__memberships__user_id=user.id)
            except ConnectionModel.DoesNotExist:
                raise Exception("Can't find connection")

            run = RunModel.objects.create(
                connection=connection,
                workspace_id=connection.workspace_id,
                user=user,
                status="queued",
                action=action if isinstance(action, str) else action.value,
            )

            process_run.delay(run.id)

            run.connection = connection

            return run

        return await sync_to_async(_run_connection)(info, connectionId, action)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def deleteConnection(
        self,
        id: strawberry.ID,
    ) -> Connection:
        connection = await ConnectionModel.objects.aget(id=id)

        await sync_to_async(connection.delete)()

        connection.id = id

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
        def _upload_connector_file(
            info: Info,
            workspaceId: strawberry.ID,
            namespace: str,
            connectorId: strawberry.ID,
            file: Upload,
        ):
            user = get_user(info)
            workspace = get_workspace(info, workspaceId)
            connector = ConnectorModel.objects.get(pk=connectorId)
            connection = ConnectionModel.objects.create(
                connector=connector,
                workspace=workspace,
                name=f"{connector.name} {uuid.uuid4()}",
                temp=True,
                namespace=namespace,
            )
            run = RunModel.objects.create(workspace=workspace, connection=connection, status="queued", user=user)
            runFile = RunFileModel(run=run)
            runFile.file = file
            runFile.save()

            process_run.delay(run.id)

            return run

        return await sync_to_async(_upload_connector_file)(info, workspaceId, namespace, connectorId, file)
