from connections.models import Connector, Connection
from api.schema import schema
import pytest
from .common import test_info


@pytest.mark.django_db
async def test_update_profile(test_info):
    info, workspace, user = test_info

    mutation = """
        mutation UpdateProfile($first_name: String!, $last_name: String!) {
            updateProfile(first_name: $first_name, last_name: $last_name) {
                id
                first_name
                last_name
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "first_name": "First Name",
            "last_name": "Test",
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["updateProfile"] == {
        "id": str(user.id),
        "first_name": "First Name",
        "last_name": "Test",
    }


@pytest.mark.django_db
async def test_create_connection(test_info):
    info, workspace, user = test_info

    connector = await Connector.objects.acreate(name="Connector 1")

    mutation = """
        mutation CreateConnection($workspaceId: ID!, $connectorId: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON!) {
            createConnection(workspaceId: $workspaceId, connectorId: $connectorId, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets) {
                id
                name
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "connectorId": str(connector.id),
            "namespace": "default",
            "name": "test connection",
            "metadata": {},
            "secrets": {},
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["createConnection"]["id"] != None
    assert resp.data["createConnection"]["name"] == "test connection"


@pytest.mark.django_db
async def test_update_connection(test_info):
    info, workspace, user = test_info

    connector = await Connector.objects.acreate(name="Connector 2")
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name="test connection2",
        metadata={},
        secrets={},
    )

    mutation = """
        mutation UpdateConnection($id: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON!) {
            updateConnection(id: $id, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets) {
                id
                name
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "id": str(connection.id),
            "namespace": "default",
            "name": "test connection3",
            "metadata": {},
            "secrets": {},
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["updateConnection"] == {
        "id": str(connection.id),
        "name": "test connection3",
    }
