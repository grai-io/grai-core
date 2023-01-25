import os

import strawberry
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from strawberry.file_uploads import Upload
from strawberry.types import Info

from api.mutations.common import get_workspace
from api.types import BasicResult
from connections.models import Connector as ConnectorModel
from connections.task_helpers import get_node, update
from connections.tasks import NoConnectorError
from lineage.models import Edge as EdgeModel
from lineage.models import Node as NodeModel


async def uploadConnectorFile(
    info: Info,
    workspaceId: strawberry.ID,
    namespace: str,
    connectorId: strawberry.ID,
    file: Upload,
) -> BasicResult:
    workspace = await get_workspace(info, workspaceId)
    connector = await ConnectorModel.objects.aget(pk=connectorId)

    path = default_storage.save("tmp/file.json", ContentFile(file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)

    if connector.name == ConnectorModel.DBT:
        from grai_source_dbt.base import get_nodes_and_edges
    elif connector.name == ConnectorModel.YAMLFILE:
        from grai_client.schemas.schema import validate_file

        # TODO: Edges don't have a human readable unique identifier
        entities = validate_file(tmp_file)
        for entity in entities:
            type = entity.type
            values = entity.spec.dict(exclude_none=True)

            Model = NodeModel if type == "Node" else EdgeModel

            if type == "Edge":
                values["source"] = await sync_to_async(get_node)(
                    workspace, values["source"]
                )
                values["destination"] = await sync_to_async(get_node)(
                    workspace, values["destination"]
                )

            try:
                record = await Model.objects.filter(workspace=workspace).aget(
                    name=entity.spec.name, namespace=entity.spec.namespace
                )
                provided_values = {k: v for k, v in values.items() if v}

                for (key, value) in provided_values.items():
                    setattr(record, key, value)

                await sync_to_async(record.save)()
            except Model.DoesNotExist:
                values["workspace"] = workspace
                await Model.objects.acreate(**values)

        return BasicResult(success=True)
    else:
        raise NoConnectorError(f"No connector found for: {connector.name}")

    nodes, edges = get_nodes_and_edges(
        manifest_file=tmp_file, namespace=namespace, version="v1"
    )
    await sync_to_async(update)(workspace, nodes)
    await sync_to_async(update)(workspace, edges)

    return BasicResult(success=True)
