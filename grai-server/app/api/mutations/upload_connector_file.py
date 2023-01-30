import strawberry
from asgiref.sync import sync_to_async
from strawberry.file_uploads import Upload
from strawberry.types import Info

from api.common import get_user
from api.mutations.common import get_workspace
from connections.models import Connector, Run, RunFile
from connections.tasks import run_update_server


async def uploadConnectorFile(
    info: Info,
    workspaceId: strawberry.ID,
    namespace: str,
    connectorId: strawberry.ID,
    file: Upload,
) -> Run:
    user = get_user(info)
    workspace = await get_workspace(info, workspaceId)
    connector = await Connector.objects.aget(pk=connectorId)

    run = await Run.objects.acreate(workspace=workspace, connector=connector, status="queued", user=user)
    runFile = RunFile(run=run)
    runFile.file = file
    await sync_to_async(runFile.save)()

    run_update_server.delay(run.id)

    return run
