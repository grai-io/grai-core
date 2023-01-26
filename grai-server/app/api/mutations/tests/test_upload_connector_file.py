import pytest

from connections.models import Connector
from lineage.models import Node
from api.tests.common import test_context
from api.mutations.upload_connector_file import uploadConnectorFile
from strawberry.types import Info
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.mark.django_db
async def test_upload_connector_file_yaml(test_context):
    context, workspace, user = test_context

    info = Info
    info.context = context

    connector = await Connector.objects.acreate(name=Connector.YAMLFILE)
    await Node.objects.acreate(name="table1", namespace="default", workspace=workspace)

    file = open(os.path.join(__location__, "test.yaml"))

    await uploadConnectorFile(
        info=info,
        workspaceId=str(workspace.id),
        namespace="default",
        connectorId=str(connector.id),
        file=file,
    )


@pytest.mark.django_db
async def test_upload_connector_file_no_connector(test_context):
    context, workspace, user = test_context

    info = Info
    info.context = context

    connector = await Connector.objects.acreate(name="Connector2")
    await Node.objects.acreate(name="table1", namespace="default", workspace=workspace)

    file = open(os.path.join(__location__, "test.yaml"))

    with pytest.raises(Exception) as e_info:
        await uploadConnectorFile(
            info=info,
            workspaceId=str(workspace.id),
            namespace="default",
            connectorId=str(connector.id),
            file=file,
        )
    assert str(e_info.value) == "No connector found for: Connector2"


@pytest.mark.django_db
async def test_upload_connector_file_dbt(test_context):
    context, workspace, user = test_context

    info = Info
    info.context = context

    connector = await Connector.objects.acreate(name=Connector.DBT)
    await Node.objects.acreate(name="table1", namespace="default", workspace=workspace)

    file = open(os.path.join(__location__, "manifest.json"))

    await uploadConnectorFile(
        info=info,
        workspaceId=str(workspace.id),
        namespace="default",
        connectorId=str(connector.id),
        file=file,
    )
