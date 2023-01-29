import uuid

import pytest

from api.schema import schema
from connections.models import Connection, Connector, Run
from lineage.models import Edge, Node
from workspaces.models import Workspace

from .common import (
    generate_connection,
    test_context,
    test_organisation,
    test_user,
    test_workspace,
)


@pytest.mark.django_db
async def test_workspace_run(test_context):
    context, organisation, workspace, user = test_context

    connector = await Connector.objects.acreate(name="Connector 4")
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name=uuid.uuid4(),
        metadata={},
        secrets={},
    )
    run = await Run.objects.acreate(workspace=workspace, connection=connection, status="success", user=user)

    query = """
        query Workspace($workspaceId: ID!, $runId: ID!) {
            workspace(id: $workspaceId) {
                id
                run(id: $runId) {
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
    context, organisation, workspace, user = test_context

    connector = await Connector.objects.acreate(name="Connector 5")
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name=uuid.uuid4(),
        metadata={},
        secrets={},
    )
    run = await Run.objects.acreate(workspace=workspace, connection=connection, status="success", user=user)

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
    assert result.data["workspace"]["connection"]["last_successful_run"]["id"] == str(run.id)


@pytest.mark.django_db
async def test_tables(test_context):
    context, organisation, workspace, user = test_context

    query = """
        query Workspace($workspaceId: ID!) {
          workspace(id: $workspaceId) {
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


@pytest.mark.django_db
async def test_workspace_nodes(test_context):
    context, organisation, workspace, user = test_context

    node = await Node.objects.acreate(workspace=workspace)

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                nodes {
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
    assert result.data["workspace"]["nodes"][0]["id"] == str(node.id)


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
async def test_tables_pagination(test_context):
    context, organisation, workspace, user = test_context

    query = """
        query Workspace($workspaceId: ID!) {
          workspace(id: $workspaceId) {
            id
            tables(pagination: {offset: 0, limit: 10}) {
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
    context, organisation, workspace, user = test_context

    table = await Node.objects.acreate(
        workspace=workspace, metadata={"grai": {"node_type": "Table"}}, name=uuid.uuid4()
    )

    query = """
        query Workspace($workspaceId: ID!, $tableId: ID!) {
          workspace(id: $workspaceId) {
            id
            table(id: $tableId) {
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
    context, organisation, workspace, user = test_context

    query = """
        query Workspace($workspaceId: ID!) {
          workspace(id: $workspaceId) {
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
async def test_workspace_edges(test_context):
    context, organisation, workspace, user = test_context

    source = await Node.objects.acreate(workspace=workspace, name="source")
    destination = await Node.objects.acreate(workspace=workspace, name="destination")

    edge = await Edge.objects.acreate(
        workspace=workspace, source=source, destination=destination, metadata={"grai": {"edge_type": "Edge"}}
    )

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
            id
            edges {
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
    assert result.data["workspace"]["edges"][0]["id"] == str(edge.id)


@pytest.mark.django_db
async def test_workspace_edge(test_context):
    context, organisation, workspace, user = test_context

    source = await Node.objects.acreate(workspace=workspace, name="source")
    destination = await Node.objects.acreate(workspace=workspace, name="destination")

    edge = await Edge.objects.acreate(
        workspace=workspace, source=source, destination=destination, metadata={"grai": {"edge_type": "Edge"}}
    )

    query = """
        query Workspace($workspaceId: ID!, $edgeId: ID!) {
            workspace(id: $workspaceId) {
            id
            edge(id: $edgeId) {
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


async def generate_table_with_column(workspace: Workspace):
    table = await Node.objects.acreate(
        workspace=workspace,
        metadata={"grai": {"node_type": "Table"}},
        name="table-" + str(uuid.uuid4()),
    )
    table_column = await Node.objects.acreate(
        workspace=workspace,
        metadata={"grai": {"node_type": "Column"}},
        name="column-" + str(uuid.uuid4()),
    )
    await Edge.objects.acreate(
        workspace=workspace,
        source=table,
        destination=table_column,
        metadata={"grai": {"edge_type": "TableToColumn"}},
        name="edge-" + str(uuid.uuid4()),
    )

    return table, table_column


async def generate_two_tables(workspace: Workspace):
    table, table_column = await generate_table_with_column(workspace)
    related_table, related_table_column = await generate_table_with_column(workspace)

    await Edge.objects.acreate(
        workspace=workspace, source=table, destination=related_table, metadata={"grai": {"edge_type": "TableToTable"}}
    )

    await Edge.objects.acreate(
        workspace=workspace,
        source=table_column,
        destination=related_table_column,
        metadata={"grai": {"edge_type": "ColumnToColumn"}},
    )

    return table, related_table


@pytest.mark.django_db
async def test_table_source_tables(test_context):
    context, organisation, workspace, user = test_context

    table, related_table = await generate_two_tables(workspace)

    query = """
        query Workspace($workspaceId: ID!, $tableId: ID!) {
          workspace(id: $workspaceId) {
            id
            table(id: $tableId) {
                id
                source_tables {
                  id
                  name
                  display_name
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
async def test_table_destination_tables(test_context):
    context, organisation, workspace, user = test_context

    table, related_table = await generate_two_tables(workspace)

    query = """
        query Workspace($workspaceId: ID!, $tableId: ID!) {
          workspace(id: $workspaceId) {
            id
            table(id: $tableId) {
                id
                destination_tables {
                  id
                  name
                  display_name
                }
            }
          }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "tableId": str(related_table.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["table"]["id"] == str(related_table.id)


@pytest.mark.django_db
async def test_tables_count(test_context):
    context, organisation, workspace, user = test_context

    await Node.objects.acreate(workspace=workspace, metadata={"grai": {"node_type": "Table"}}, name=uuid.uuid4())

    query = """
        query Workspace($workspaceId: ID!) {
          workspace(id: $workspaceId) {
            id
            tables_count
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
    assert result.data["workspace"]["tables_count"] == 1


@pytest.mark.django_db
async def test_other_edges_count(test_context):
    context, organisation, workspace, user = test_context

    await Node.objects.acreate(
        workspace=workspace,
        metadata={"grai": {"node_type": "Table"}},
        name=uuid.uuid4(),
    )

    query = """
        query Workspace($workspaceId: ID!) {
          workspace(id: $workspaceId) {
            id
            other_edges_count
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
    assert result.data["workspace"]["other_edges_count"] == 0


@pytest.mark.django_db
async def test_workspace_connections(test_context):
    context, organisation, workspace, user = test_context

    connector = await Connector.objects.acreate(name=f"Connector - {uuid.uuid4()}")
    connection = await Connection.objects.acreate(workspace=workspace, connector=connector)

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                connections {
                    id
                    connector {
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
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["connections"][0]["id"] == str(connection.id)
    assert result.data["workspace"]["connections"][0]["connector"]["id"] == str(connector.id)


@pytest.mark.django_db
async def test_workspace_runs(test_context):
    context, organisation, workspace, user = test_context

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                runs {
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
async def test_workspace_memberships(test_context):
    context, organisation, workspace, user = test_context

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                memberships {
                    id
                    role
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
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["memberships"][0]["role"] == "admin"
    assert result.data["workspace"]["memberships"][0]["user"]["id"] == str(user.id)
