import pytest

from api.schema import schema
from api.tests.common import (
    generate_connection,
    generate_connection_name,
    generate_connector,
    generate_username,
    generate_workspace,
    test_basic_context,
    test_context,
    test_organisation,
    test_user,
    test_workspace,
)
from connections.models import Connection


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_connection(test_context):
    context, organisation, workspace, user, membership = test_context

    connector = await generate_connector()

    mutation = """
        mutation CreateConnection($workspaceId: ID!, $connectorId: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            createConnection(workspaceId: $workspaceId, connectorId: $connectorId, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
                id
                name
            }
        }
    """

    name = generate_connection_name()

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "connectorId": str(connector.id),
            "namespace": "default",
            "name": name,
            "metadata": {},
            "secrets": None,
            "schedules": None,
            "is_active": False,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createConnection"]["id"] != None
    assert result.data["createConnection"]["name"] == name


@pytest.mark.django_db
async def test_create_connection_no_membership(test_context):
    context, organisation, workspace, user, membership = test_context

    workspace2 = await generate_workspace(organisation)

    connector = await generate_connector()

    mutation = """
        mutation CreateConnection($workspaceId: ID!, $connectorId: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            createConnection(workspaceId: $workspaceId, connectorId: $connectorId, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace2.id),
            "connectorId": str(connector.id),
            "namespace": "default",
            "name": generate_connection_name(),
            "metadata": {},
            "secrets": None,
            "schedules": None,
            "is_active": False,
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can\'t find workspace", locations=[SourceLocation(line=3, column=13)], path=[\'createConnection\'])]"""
    )
    assert result.data is None


@pytest.mark.django_db
async def test_update_connection(test_context):
    context, organisation, workspace, user, membership = test_context
    connection = await generate_connection(workspace)

    mutation = """
        mutation UpdateConnection($id: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            updateConnection(id: $id, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
                id
                name
            }
        }
    """

    name = generate_connection_name()

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(connection.id),
            "namespace": "default",
            "name": name,
            "metadata": {},
            "secrets": {
                "a": "hello",
            },
            "schedules": None,
            "is_active": False,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateConnection"] == {
        "id": str(connection.id),
        "name": name,
    }


@pytest.mark.django_db
async def test_update_connection_with_schedule(test_context):
    context, organisation, workspace, user, membership = test_context
    connection = await generate_connection(workspace)

    mutation = """
        mutation UpdateConnection($id: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            updateConnection(id: $id, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
                id
                name
            }
        }
    """

    name = generate_connection_name()

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(connection.id),
            "namespace": "default",
            "name": name,
            "metadata": {},
            "secrets": None,
            "schedules": {
                "type": "cron",
                "cron": {
                    "minutes": "*",
                    "hours": "*",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
            },
            "is_active": False,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateConnection"] == {
        "id": str(connection.id),
        "name": name,
    }


@pytest.mark.django_db
async def test_update_connection_with_incorrect_schedule(test_context):
    context, organisation, workspace, user, membership = test_context
    connection = await generate_connection(workspace)

    mutation = """
        mutation UpdateConnection($id: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            updateConnection(id: $id, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(connection.id),
            "namespace": "default",
            "name": generate_connection_name(),
            "metadata": {},
            "secrets": None,
            "schedules": {"type": "blah"},
            "is_active": False,
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Schedule type not found', locations=[SourceLocation(line=3, column=13)], path=['updateConnection'])]"
    )
    assert result.data is None


@pytest.mark.django_db
async def test_update_connection_no_membership(test_context):
    context, organisation, workspace, user, membership = test_context
    workspace2 = await generate_workspace(organisation)
    connection = await generate_connection(workspace2)

    mutation = """
        mutation UpdateConnection($id: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            updateConnection(id: $id, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(connection.id),
            "namespace": "default",
            "name": generate_connection_name(),
            "metadata": {},
            "secrets": None,
            "schedules": None,
            "is_active": False,
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can't find connection", locations=[SourceLocation(line=3, column=13)], path=['updateConnection'])]"""
    )
    assert result.data is None


@pytest.mark.django_db
async def test_update_connection_temp(test_context):
    context, organisation, workspace, user, membership = test_context
    connection = await generate_connection(workspace, temp=True)

    mutation = """
        mutation UpdateConnection($id: ID!, $temp: Boolean) {
            updateConnection(id: $id, temp: $temp) {
                id
                temp
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(connection.id),
            "temp": True,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateConnection"] == {
        "id": str(connection.id),
        "temp": True,
    }
    assert connection.temp is True


@pytest.mark.django_db
async def test_run_connection(test_context):
    context, organisation, workspace, user, membership = test_context
    connection = await generate_connection(workspace)

    mutation = """
        mutation RunConnection($connectionId: ID!) {
            runConnection(connectionId: $connectionId) {
                id
                connection {
                    id
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "connectionId": str(connection.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["runConnection"]["connection"] == {
        "id": str(connection.id),
    }


@pytest.mark.django_db
async def test_run_connection_no_membership(test_context):
    context, organisation, workspace, user, membership = test_context
    workspace2 = await generate_workspace(organisation)
    connection = await generate_connection(workspace2)

    mutation = """
        mutation RunConnection($connectionId: ID!) {
            runConnection(connectionId: $connectionId) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "connectionId": str(connection.id),
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can't find connection", locations=[SourceLocation(line=3, column=13)], path=['runConnection'])]"""
    )
    assert result.data is None


@pytest.mark.django_db
async def test_run_connection_postgres(test_context):
    context, organisation, workspace, user, membership = test_context
    connection = await generate_connection(workspace)

    mutation = """
        mutation RunConnection($connectionId: ID!) {
            runConnection(connectionId: $connectionId) {
                id
                connection {
                    id
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "connectionId": str(connection.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["runConnection"]["connection"] == {
        "id": str(connection.id),
    }


@pytest.mark.django_db
async def test_delete_connection(test_context):
    context, organisation, workspace, user, membership = test_context
    connection = await generate_connection(workspace)

    mutation = """
        mutation DeleteConnection($id: ID!) {
            deleteConnection(id: $id) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(connection.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["deleteConnection"]["id"] == str(connection.id)

    with pytest.raises(Exception) as e_info:
        await Connection.objects.aget(id=connection.id)

    assert str(e_info.value) == "Connection matching query does not exist."
