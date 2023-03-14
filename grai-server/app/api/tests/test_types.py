import uuid
from unittest import mock
from unittest.mock import MagicMock

import pytest
from algoliasearch.search_client import SearchClient

from api.schema import schema
from connections.models import Connection, Connector, Run
from installations.models import Branch, Commit, PullRequest, Repository
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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

    table = await Node.objects.acreate(
        workspace=workspace, metadata={"grai": {"node_type": "Table"}}, name=uuid.uuid4()
    )

    column = await Node.objects.acreate(
        workspace=workspace, metadata={"grai": {"node_type": "Column"}}, name=uuid.uuid4()
    )

    edge = await Edge.objects.acreate(
        workspace=workspace, source=table, destination=column, metadata={"grai": {"edge_type": "TableToColumn"}}
    )

    query = """
        query Workspace($workspaceId: ID!, $tableId: ID!) {
          workspace(id: $workspaceId) {
            id
            table(id: $tableId) {
                id
                columns {
                  id
                  requirements_edges {
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
            "tableId": str(table.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["table"]["id"] == str(table.id)


@pytest.mark.django_db
async def test_other_edges(test_context):
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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


@pytest.mark.django_db
async def test_workspace_search_key(test_context, mocker):
    mock = mocker.patch("api.types.Search")
    search_client = MagicMock()
    search_client.generate_secured_api_key.return_value = "search_key"
    mock.return_value = search_client

    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                search_key
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
    assert result.data["workspace"]["search_key"] == "search_key"


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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
async def test_workspace_runs_filter_by_repo(test_context, test_commit):
    context, organisation, workspace, user, membership = test_context

    connector = await Connector.objects.acreate(name=str(uuid.uuid4()))
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name=uuid.uuid4(),
        metadata={},
        secrets={},
    )
    run = await Run.objects.acreate(workspace=workspace, commit=test_commit, connection=connection, status="success")

    query = """
        query Workspace($workspaceId: ID!, $owner: String, $repo: String) {
            workspace(id: $workspaceId) {
                id
                runs(owner: $owner, repo: $repo) {
                    id
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "owner": test_commit.repository.owner,
            "repo": test_commit.repository.repo,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)


@pytest.mark.django_db
async def test_workspace_runs_filter_by_branch(test_context, test_branch, test_commit):
    context, organisation, workspace, user, membership = test_context

    connector = await Connector.objects.acreate(name=str(uuid.uuid4()))
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name=uuid.uuid4(),
        metadata={},
        secrets={},
    )
    run = await Run.objects.acreate(workspace=workspace, commit=test_commit, connection=connection, status="success")

    query = """
        query Workspace($workspaceId: ID!, $branch: String) {
            workspace(id: $workspaceId) {
                id
                runs(branch: $branch) {
                    id
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "branch": test_commit.branch.reference,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)


@pytest.mark.django_db
async def test_workspace_runs_filter_by_action(test_context):
    context, organisation, workspace, user, membership = test_context

    connector = await Connector.objects.acreate(name=str(uuid.uuid4()))
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name=uuid.uuid4(),
        metadata={},
        secrets={},
    )
    run = await Run.objects.acreate(workspace=workspace, connection=connection, status="success", action=Run.TESTS)
    await Run.objects.acreate(workspace=workspace, connection=connection, status="success", action=Run.VALIDATE)

    query = """
        query Workspace($workspaceId: ID!, $action: String) {
            workspace(id: $workspaceId) {
                id
                runs(action: $action) {
                    id
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "action": Run.TESTS,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert len(result.data["workspace"]["runs"]) == 1
    assert result.data["workspace"]["runs"][0]["id"] == str(run.id)


@pytest.mark.django_db
async def test_workspace_memberships(test_context):
    context, organisation, workspace, user, membership = test_context

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


@pytest.fixture
async def test_repository(test_workspace):
    return await Repository.objects.acreate(
        workspace=test_workspace, type=Repository.GITHUB, owner=str(uuid.uuid4()), repo=str(uuid.uuid4())
    )


@pytest.fixture
async def test_branch(test_workspace, test_repository):
    return await Branch.objects.acreate(
        workspace=test_workspace, repository=test_repository, reference=str(uuid.uuid4())
    )


@pytest.fixture
async def test_pull_request(test_workspace, test_repository, test_branch):
    return await PullRequest.objects.acreate(
        workspace=test_workspace,
        repository=test_repository,
        branch=test_branch,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


@pytest.fixture
async def test_commit(test_workspace, test_repository, test_branch):
    return await Commit.objects.acreate(
        workspace=test_workspace,
        repository=test_repository,
        branch=test_branch,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


@pytest.fixture
async def test_commit_with_pr(test_workspace, test_repository, test_branch, test_pull_request):
    return await Commit.objects.acreate(
        workspace=test_workspace,
        repository=test_repository,
        branch=test_branch,
        pull_request=test_pull_request,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


@pytest.mark.django_db
async def test_workspace_repositories(test_context, test_repository):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                repositories {
                    id
                    type
                    owner
                    repo
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
    assert result.data["workspace"]["repositories"][0]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repositories"][0]["type"] == Repository.GITHUB
    assert result.data["workspace"]["repositories"][0]["owner"] == test_repository.owner
    assert result.data["workspace"]["repositories"][0]["repo"] == test_repository.repo


@pytest.mark.django_db
async def test_workspace_repositories_filter(test_context, test_repository):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $type: String!, $owner: String!, $repo: String!) {
            workspace(id: $workspaceId) {
                id
                repositories(type: $type, owner: $owner, repo: $repo) {
                    id
                    type
                    owner
                    repo
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "type": test_repository.type,
            "owner": test_repository.owner,
            "repo": test_repository.repo,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repositories"][0]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repositories"][0]["type"] == Repository.GITHUB
    assert result.data["workspace"]["repositories"][0]["owner"] == test_repository.owner
    assert result.data["workspace"]["repositories"][0]["repo"] == test_repository.repo


@pytest.mark.django_db
async def test_workspace_repository_by_id(test_context, test_repository):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    type
                    owner
                    repo
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={"workspaceId": str(workspace.id), "repositoryId": str(test_repository.id)},
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["type"] == Repository.GITHUB
    assert result.data["workspace"]["repository"]["owner"] == test_repository.owner
    assert result.data["workspace"]["repository"]["repo"] == test_repository.repo


@pytest.mark.django_db
async def test_workspace_repository_by_reference(test_context, test_repository):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $type: String!, $owner: String!, $repo: String!) {
            workspace(id: $workspaceId) {
                id
                repository(type: $type, owner: $owner, repo: $repo) {
                    id
                    type
                    owner
                    repo
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "type": test_repository.type,
            "owner": test_repository.owner,
            "repo": test_repository.repo,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["type"] == Repository.GITHUB
    assert result.data["workspace"]["repository"]["owner"] == test_repository.owner
    assert result.data["workspace"]["repository"]["repo"] == test_repository.repo


@pytest.mark.django_db
async def test_workspace_branches(test_context, test_branch):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                branches {
                    id
                    reference
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
    assert result.data["workspace"]["branches"][0]["id"] == str(test_branch.id)
    assert result.data["workspace"]["branches"][0]["reference"] == test_branch.reference


@pytest.mark.django_db
async def test_workspace_branch_by_id(test_context, test_branch):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $branchId: ID!) {
            workspace(id: $workspaceId) {
                id
                branch(id: $branchId) {
                    id
                    reference
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={"workspaceId": str(workspace.id), "branchId": str(test_branch.id)},
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["branch"]["id"] == str(test_branch.id)
    assert result.data["workspace"]["branch"]["reference"] == test_branch.reference


@pytest.mark.django_db
async def test_workspace_branch_by_reference(test_context, test_branch):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $reference: String!) {
            workspace(id: $workspaceId) {
                id
                branch(reference: $reference) {
                    id
                    reference
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "reference": test_branch.reference,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["branch"]["id"] == str(test_branch.id)
    assert result.data["workspace"]["branch"]["reference"] == test_branch.reference


@pytest.mark.django_db
async def test_workspace_pull_requests(test_context, test_pull_request):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                pull_requests {
                    id
                    reference
                    title
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
    assert result.data["workspace"]["pull_requests"][0]["id"] == str(test_pull_request.id)
    assert result.data["workspace"]["pull_requests"][0]["reference"] == test_pull_request.reference
    assert result.data["workspace"]["pull_requests"][0]["title"] == test_pull_request.title


@pytest.mark.django_db
async def test_workspace_pull_request_by_id(test_context, test_pull_request):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $pull_requestId: ID!) {
            workspace(id: $workspaceId) {
                id
                pull_request(id: $pull_requestId) {
                    id
                    reference
                    title
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={"workspaceId": str(workspace.id), "pull_requestId": str(test_pull_request.id)},
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["pull_request"]["id"] == str(test_pull_request.id)
    assert result.data["workspace"]["pull_request"]["reference"] == test_pull_request.reference
    assert result.data["workspace"]["pull_request"]["title"] == test_pull_request.title


@pytest.mark.django_db
async def test_workspace_pull_request_by_reference(test_context, test_pull_request):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $reference: String!) {
            workspace(id: $workspaceId) {
                id
                pull_request(reference: $reference) {
                    id
                    reference
                    title
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "reference": test_pull_request.reference,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["pull_request"]["id"] == str(test_pull_request.id)
    assert result.data["workspace"]["pull_request"]["reference"] == test_pull_request.reference
    assert result.data["workspace"]["pull_request"]["title"] == test_pull_request.title


@pytest.mark.django_db
async def test_workspace_commits(test_context, test_commit):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!) {
            workspace(id: $workspaceId) {
                id
                commits {
                    id
                    reference
                    title
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
    assert result.data["workspace"]["commits"][0]["id"] == str(test_commit.id)
    assert result.data["workspace"]["commits"][0]["reference"] == test_commit.reference
    assert result.data["workspace"]["commits"][0]["title"] == test_commit.title


@pytest.mark.django_db
async def test_workspace_commit_by_id(test_context, test_commit):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $commitId: ID!) {
            workspace(id: $workspaceId) {
                id
                commit(id: $commitId) {
                    id
                    reference
                    title
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={"workspaceId": str(workspace.id), "commitId": str(test_commit.id)},
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["commit"]["id"] == str(test_commit.id)
    assert result.data["workspace"]["commit"]["reference"] == test_commit.reference
    assert result.data["workspace"]["commit"]["title"] == test_commit.title


@pytest.mark.django_db
async def test_workspace_commit_by_reference(test_context, test_commit):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $reference: String!) {
            workspace(id: $workspaceId) {
                id
                commit(reference: $reference) {
                    id
                    reference
                    title
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "workspaceId": str(workspace.id),
            "reference": test_commit.reference,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["commit"]["id"] == str(test_commit.id)
    assert result.data["workspace"]["commit"]["reference"] == test_commit.reference
    assert result.data["workspace"]["commit"]["title"] == test_commit.title


@pytest.mark.django_db
async def test_repository_branch_by_id(test_context, test_repository, test_branch):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!, $branchId: ID!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    branch(id: $branchId) {
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
            "repositoryId": str(test_repository.id),
            "branchId": str(test_branch.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["branch"]["id"] == str(test_branch.id)


@pytest.mark.django_db
async def test_repository_branch_by_reference(test_context, test_repository, test_branch):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!, $reference: String!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    branch(reference: $reference) {
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
            "repositoryId": str(test_repository.id),
            "reference": test_branch.reference,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["branch"]["id"] == str(test_branch.id)


@pytest.mark.django_db
async def test_repository_pull_request_by_id(test_context, test_repository, test_pull_request):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!, $pullRequestId: ID!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    pull_request(id: $pullRequestId) {
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
            "repositoryId": str(test_repository.id),
            "pullRequestId": str(test_pull_request.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["pull_request"]["id"] == str(test_pull_request.id)


@pytest.mark.django_db
async def test_repository_pull_request_by_reference(test_context, test_repository, test_pull_request):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!, $reference: String!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    pull_request(reference: $reference) {
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
            "repositoryId": str(test_repository.id),
            "reference": test_pull_request.reference,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["pull_request"]["id"] == str(test_pull_request.id)


@pytest.mark.django_db
async def test_repository_commit_by_id(test_context, test_repository, test_commit):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!, $commitId: ID!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    commit(id: $commitId) {
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
            "repositoryId": str(test_repository.id),
            "commitId": str(test_commit.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["commit"]["id"] == str(test_commit.id)


@pytest.mark.django_db
async def test_repository_commit_by_reference(test_context, test_repository, test_commit):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!, $reference: String!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    commit(reference: $reference) {
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
            "repositoryId": str(test_repository.id),
            "reference": test_commit.reference,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["commit"]["id"] == str(test_commit.id)


@pytest.mark.django_db
async def test_branch_last_commit(test_context, test_repository, test_branch, test_commit):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!, $branchId: ID!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    branch(id: $branchId) {
                        id
                        last_commit {
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
            "repositoryId": str(test_repository.id),
            "branchId": str(test_branch.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["branch"]["id"] == str(test_branch.id)
    assert result.data["workspace"]["repository"]["branch"]["last_commit"]["id"] == str(test_commit.id)


@pytest.mark.django_db
async def test_pull_request_last_commit(test_context, test_repository, test_pull_request, test_commit_with_pr):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($workspaceId: ID!, $repositoryId: ID!, $pullRequestId: ID!) {
            workspace(id: $workspaceId) {
                id
                repository(id: $repositoryId) {
                    id
                    pull_request(id: $pullRequestId) {
                        id
                        last_commit {
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
            "repositoryId": str(test_repository.id),
            "pullRequestId": str(test_pull_request.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["repository"]["id"] == str(test_repository.id)
    assert result.data["workspace"]["repository"]["pull_request"]["id"] == str(test_pull_request.id)
    assert result.data["workspace"]["repository"]["pull_request"]["last_commit"]["id"] == str(test_commit_with_pr.id)


@pytest.mark.django_db
async def test_commit_last_run(test_context, test_commit):
    context, organisation, workspace, user, membership = test_context

    connector = await Connector.objects.acreate(name=str(uuid.uuid4()))
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name=uuid.uuid4(),
        metadata={},
        secrets={},
    )
    successful_run = await Run.objects.acreate(
        workspace=workspace, connection=connection, commit=test_commit, status="success", user=user
    )
    last_run = await Run.objects.acreate(
        workspace=workspace, connection=connection, commit=test_commit, status="failure", user=user
    )

    query = """
        query Workspace($workspaceId: ID!, $commitId: ID!) {
            workspace(id: $workspaceId) {
                id
                commit(id: $commitId) {
                    id
                    last_run {
                        id
                    }
                    last_successful_run {
                        id
                    }
                }
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={"workspaceId": str(workspace.id), "commitId": str(test_commit.id)},
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"]["id"] == str(workspace.id)
    assert result.data["workspace"]["commit"]["id"] == str(test_commit.id)
    assert result.data["workspace"]["commit"]["last_run"]["id"] == str(last_run.id)
    assert result.data["workspace"]["commit"]["last_successful_run"]["id"] == str(successful_run.id)
