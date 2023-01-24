import pytest

from api.schema import schema
from connections.models import Run
from lineage.models import Node, Edge

from .common import test_context, test_organisation, test_user, generate_connection


@pytest.mark.django_db
async def test_workspace_run(test_context):
    context, organisation, workspace, user = test_context
    connection = await generate_connection(workspace=workspace)
    run = await Run.objects.acreate(
        workspace=workspace, connection=connection, status="success", user=user
    )

    query = """
        query Workspace($workspaceId: ID!, $runId: ID!) {
            workspace(id: $workspaceId) {
                id
                run(id: $runId) {
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
    context, organisation, workspace, user = test_context
    connection = await generate_connection(workspace=workspace)
    run = await Run.objects.acreate(
        workspace=workspace, connection=connection, status="success", user=user
    )

    query = """
        query Workspace($workspaceId: ID!, $connectionId: ID!, $runId: ID!) {
            workspace(id: $workspaceId) {
                id
                connection(id: $connectionId) {
                  id
                  name
                  run(id: $runId) {
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
    assert result.data["workspace"]["connection"]["last_successful_run"]["id"] == str(
        run.id
    )


@pytest.mark.django_db
async def test_workspace_node(test_context):
    context, organisation, workspace, user = test_context

    node = await Node.objects.acreate(workspace=workspace)

    query = """
        query Workspace($workspaceId: ID!, $nodeId: ID!) {
            workspace(id: $workspaceId) {
                id
                node(id: $nodeId) {
                  id
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "nodeId": str(node.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["node"]["id"] == str(node.id)


@pytest.mark.django_db
async def test_workspace_edge(test_context):
    context, organisation, workspace, user = test_context

    source = await Node.objects.acreate(workspace=workspace, name="source")
    destination = await Node.objects.acreate(workspace=workspace, name="destination")

    edge = await Edge.objects.acreate(
        workspace=workspace, source=source, destination=destination
    )

    query = """
        query Workspace($workspaceId: ID!, $edgeId: ID!) {
            workspace(id: $workspaceId) {
                id
                edge(id: $edgeId) {
                  id
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "edgeId": str(edge.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["edge"]["id"] == str(edge.id)
