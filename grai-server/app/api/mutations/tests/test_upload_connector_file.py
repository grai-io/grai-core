import os

import pytest
from strawberry.types import Info

from api.mutations.upload_connector_file import uploadConnectorFile
from api.tests.common import test_context, test_organisation, test_user, test_workspace
from connections.models import Connector
from lineage.models import Node

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.fixture
async def test_node(test_workspace):
    node, created = await Node.objects.aget_or_create(
        name="table1", namespace="default", workspace=test_workspace
    )

    return node


@pytest.mark.django_db
async def test_upload_connector_file_yaml(test_context, test_node):
    context, test_organisation, workspace, test_user = test_context

    info = Info
    info.context = context

    connector = await Connector.objects.acreate(name=Connector.YAMLFILE)

    file = open(os.path.join(__location__, "test.yaml"))

    await uploadConnectorFile(
        info=info,
        workspaceId=str(workspace.id),
        namespace="default",
        connectorId=str(connector.id),
        file=file,
    )


@pytest.mark.django_db
async def test_upload_connector_file_no_connector(test_context, test_node):
    context, test_organisation, workspace, test_user = test_context

    info = Info
    info.context = context

    connector = await Connector.objects.acreate(name="Connector2")

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
async def test_upload_connector_file_dbt(test_context, test_node):
    context, test_organisation, workspace, test_user = test_context

    info = Info
    info.context = context

    connector = await Connector.objects.acreate(name=Connector.DBT)

    file = open(os.path.join(__location__, "manifest.json"))

    await uploadConnectorFile(
        info=info,
        workspaceId=str(workspace.id),
        namespace="default",
        connectorId=str(connector.id),
        file=file,
    )
