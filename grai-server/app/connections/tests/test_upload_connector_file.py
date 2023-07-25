import os

import pytest
from django.core.files.uploadedfile import UploadedFile
from strawberry.types import Info

from api.tests.common import (
    test_context,
    test_organisation,
    test_user,
    test_workspace,
    test_source,
)
from connections.models import Connector
from connections.mutations import Mutation
from lineage.models import Node

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.fixture
async def test_node(test_workspace):
    node, created = await Node.objects.aget_or_create(name="table1", namespace="default", workspace=test_workspace)

    return node


@pytest.mark.django_db
async def test_upload_connector_file_yaml(test_context):
    context, test_organisation, workspace, test_user, membership = test_context

    info = Info
    info.context = context

    connector, created = await Connector.objects.aget_or_create(name=Connector.YAMLFILE, slug=Connector.YAMLFILE)

    with open(os.path.join(__location__, "test.yaml")) as reader:
        file = UploadedFile(reader, name="test.yaml")

        mutation = Mutation()

        await mutation.uploadConnectorFile(
            info=info,
            workspaceId=str(workspace.id),
            namespace="default",
            connectorId=str(connector.id),
            file=file,
            sourceName="test",
        )


@pytest.mark.django_db
async def test_upload_connector_file_yaml_source_id(test_context, test_source):
    context, test_organisation, workspace, test_user, membership = test_context

    info = Info
    info.context = context

    connector, created = await Connector.objects.aget_or_create(name=Connector.YAMLFILE, slug=Connector.YAMLFILE)

    with open(os.path.join(__location__, "test.yaml")) as reader:
        file = UploadedFile(reader, name="test.yaml")

        mutation = Mutation()

        await mutation.uploadConnectorFile(
            info=info,
            workspaceId=str(workspace.id),
            namespace="default",
            connectorId=str(connector.id),
            file=file,
            sourceId=str(test_source.id),
        )


# @pytest.mark.django_db
# async def test_upload_connector_file_no_connector(test_context, test_node):
#     context, test_organisation, workspace, test_user, membership = test_context

#     info = Info
#     info.context = context

#     connector = await Connector.objects.acreate(name="Connector2")

#     with open(os.path.join(__location__, "test.yaml")) as reader:
#         file = UploadedFile(reader, name="test.yaml")

#         with pytest.raises(Exception) as e_info:
#             await uploadConnectorFile(
#                 info=info,
#                 workspaceId=str(workspace.id),
#                 namespace="default",
#                 connectorId=str(connector.id),
#                 file=file,
#             )
#         assert str(e_info.value) == "No connector found for: Connector2"


@pytest.mark.django_db
async def test_upload_connector_file_dbt(test_context, test_node):
    context, test_organisation, workspace, test_user, membership = test_context

    info = Info
    info.context = context

    connector, created = await Connector.objects.aget_or_create(name=Connector.DBT, slug=Connector.DBT)

    with open(os.path.join(__location__, "manifest.json")) as reader:
        file = UploadedFile(reader, name="manifest.json")

        mutation = Mutation()

        await mutation.uploadConnectorFile(
            info=info,
            workspaceId=str(workspace.id),
            namespace="default",
            connectorId=str(connector.id),
            file=file,
            sourceName="test",
        )
