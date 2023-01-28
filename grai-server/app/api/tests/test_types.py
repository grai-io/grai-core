import pytest

from api.schema import schema
from connections.models import Connection, Connector, Run

from .common import test_context


@pytest.mark.django_db
async def test_workspace_run(test_context):
    context, workspace, user = test_context

    connector = await Connector.objects.acreate(name="Connector 4")
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name="test connection2",
        metadata={},
        secrets={},
    )
    run = await Run.objects.acreate(workspace=workspace, connection=connection, status="success", user=user)

    query = """
        query Workspace($workspaceId: ID!, $runId: ID!) {
            workspace(pk: $workspaceId) {
                id
                run(pk: $runId) {
                  id
                  status
                  user {
                    id
                  }
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "runId": str(run.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["run"]["id"] == str(run.id)


@pytest.mark.django_db
async def test_workspace_connection_run(test_context):
    context, workspace, user = test_context

    connector = await Connector.objects.acreate(name="Connector 5")
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name="test connection2",
        metadata={},
        secrets={},
    )
    run = await Run.objects.acreate(workspace=workspace, connection=connection, status="success", user=user)

    query = """
        query Workspace($workspaceId: ID!, $connectionId: ID!, $runId: ID!) {
            workspace(pk: $workspaceId) {
                id
                connection(pk: $connectionId) {
                  id
                  name
                  run(pk: $runId) {
                    id
                    status
                    user {
                      id
                    }
                  }
                  last_run {
                    id
                    status
                    user {
                      id
                    }
                  }
                  last_successful_run {
                    id
                    status
                    user {
                      id
                    }
                  }
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "connectionId": str(connection.id),
            "runId": str(run.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["connection"]["id"] == str(connection.id)
    assert result.data["workspace"]["connection"]["run"]["id"] == str(run.id)
    assert result.data["workspace"]["connection"]["last_run"]["id"] == str(run.id)
    assert result.data["workspace"]["connection"]["last_successful_run"]["id"] == str(run.id)
