import pytest

from api.schema import schema
from connections.models import Connection, Connector, Run
from lineage.models import Node, Edge

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
                    full_name
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


@pytest.mark.django_db
async def test_tables(test_context):
    context, workspace, user = test_context

    query = """
        query Workspace($workspaceId: ID!) {
          workspace(pk: $workspaceId) {
            id
            tables {
                id
            }
          }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)


@pytest.mark.django_db
async def test_table(test_context):
    context, workspace, user = test_context

    table = await Node.objects.acreate(workspace=workspace, metadata={"grai": {"node_type": "Table"}})

    query = """
        query Workspace($workspaceId: ID!, $tableId: ID!) {
          workspace(pk: $workspaceId) {
            id
            table(pk: $tableId) {
                id
                columns {
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
            "tableId": str(table.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["table"]["id"] == str(table.id)


@pytest.mark.django_db
async def test_other_edges(test_context):
    context, workspace, user = test_context

    query = """
        query Workspace($workspaceId: ID!) {
          workspace(pk: $workspaceId) {
            id
            other_edges {
                id
            }
          }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)


@pytest.mark.django_db
async def test_node(test_context):
    context, workspace, user = test_context

    node = await Node.objects.acreate(workspace=workspace, metadata={"grai": {"node_type": "Table"}})

    query = """
        query Workspace($workspaceId: ID!, $nodeId: ID!) {
          workspace(pk: $workspaceId) {
            id
            node(pk: $nodeId) {
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
async def test_edge(test_context):
    context, workspace, user = test_context

    source = await Node.objects.acreate(workspace=workspace, name="source", metadata={"grai": {"node_type": "Table"}})
    destination = await Node.objects.acreate(
        workspace=workspace, name="desination", metadata={"grai": {"node_type": "Table"}}
    )
    edge = await Edge.objects.acreate(
        workspace=workspace, source=source, destination=destination, metadata={"grai": {"edge_type": "Edge"}}
    )

    query = """
        query Workspace($workspaceId: ID!, $edgeId: ID!) {
          workspace(pk: $workspaceId) {
            id
            edge(pk: $edgeId) {
                id
                source {
                  id
                }
                destination {
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
            "edgeId": str(edge.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["edge"]["id"] == str(edge.id)
    assert result.data["workspace"]["edge"]["source"]["id"] == str(source.id)
    assert result.data["workspace"]["edge"]["destination"]["id"] == str(destination.id)
