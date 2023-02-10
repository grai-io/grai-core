from unittest.mock import MagicMock
import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
import types

from api.schema import schema

from .common import (
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


@pytest.mark.django_db
async def test_login(test_basic_context):
    context = test_basic_context

    User = get_user_model()

    user = User(username=generate_username())
    user.set_password("password")
    await sync_to_async(user.save)()

    mutation = """
        mutation Login($username: String!, $password: String!) {
            login(username: $username, password: $password) {
                id
                username
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "username": user.username,
            "password": "password",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["login"] == {
        "id": str(user.id),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


@pytest.mark.django_db
async def test_login_bad_password(test_basic_context):
    context = test_basic_context

    User = get_user_model()

    user = User(username=generate_username())
    user.set_password("password")
    await sync_to_async(user.save)()

    mutation = """
        mutation Login($username: String!, $password: String!) {
            login(username: $username, password: $password) {
                id
                username
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "username": user.username,
            "password": "password2",
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Invalid credentials', locations=[SourceLocation(line=3, column=13)], path=['login'])]"
    )
    assert result.data is None


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_logout(test_context):
    context, organisation, workspace, user = test_context

    mutation = """
        mutation Logout {
            logout
        }
    """

    result = await schema.execute(
        mutation,
        context_value=context,
    )

    assert result.errors is None
    assert result.data["logout"] == True


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_register(test_basic_context):
    context = test_basic_context

    mutation = """
        mutation Register($username: String!, $password: String!) {
            register(username: $username, password: $password) {
            id
            username
            first_name
            last_name
            }
        }
    """

    username = generate_username()

    result = await schema.execute(
        mutation,
        variable_values={
            "username": username,
            "password": "password",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["register"]["id"] is not None
    assert result.data["register"]["username"] == username


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_connection(test_context):
    context, organisation, workspace, user = test_context

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
    context, organisation, workspace, user = test_context

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
    context, organisation, workspace, user = test_context
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
    context, organisation, workspace, user = test_context
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
    context, organisation, workspace, user = test_context
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
    context, organisation, workspace, user = test_context
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
async def test_run_connection(test_context):
    context, organisation, workspace, user = test_context
    connection = await generate_connection(workspace)

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

    assert result.errors is None
    assert result.data["runConnection"] == {
        "id": str(connection.id),
    }


@pytest.mark.django_db
async def test_run_connection_no_membership(test_context):
    context, organisation, workspace, user = test_context
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
    context, organisation, workspace, user = test_context
    connection = await generate_connection(workspace)

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

    assert result.errors is None
    assert result.data["runConnection"] == {
        "id": str(connection.id),
    }


@pytest.mark.django_db
async def test_create_api_key(test_context):
    context, organisation, workspace, user = test_context

    mutation = """
        mutation CreateApiKey($workspaceId: ID!, $name: String!) {
            createApiKey(workspaceId: $workspaceId, name: $name) {
                key
                api_key {
                    id
                    name
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "name": "test api key",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createApiKey"]["key"] != None
    assert result.data["createApiKey"]["api_key"]["name"] == "test api key"


@pytest.mark.django_db
async def test_update_workspace(test_context):
    context, organisation, workspace, user = test_context

    mutation = """
        mutation UpdateWorkspace($id: ID!, $name: String!) {
            updateWorkspace(id: $id, name: $name) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(workspace.id),
            "name": "Test Workspace 2",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateWorkspace"] == {
        "id": str(workspace.id),
        "name": "Test Workspace 2",
    }


@pytest.mark.django_db
async def test_create_membership(test_context):
    context, organisation, workspace, user = test_context

    mutation = """
        mutation CreateMembership($workspaceId: ID!, $role: String!, $email: String!) {
            createMembership(workspaceId: $workspaceId, role: $role, email: $email) {
                id
                role
                user {
                    id
                    username
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "role": "admin",
            "email": "test@example.com",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createMembership"]["role"] == "admin"
    assert result.data["createMembership"]["user"]["username"] == "test@example.com"


@pytest.mark.django_db
async def test_create_membership_existing_user(test_context):
    context, organisation, workspace, user = test_context
    User = get_user_model()
    user = await User.objects.acreate(username=generate_username())

    mutation = """
        mutation CreateMembership($workspaceId: ID!, $role: String!, $email: String!) {
            createMembership(workspaceId: $workspaceId, role: $role, email: $email) {
                id
                role
                user {
                    id
                    username
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "role": "admin",
            "email": user.username,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createMembership"]["role"] == "admin"
    assert result.data["createMembership"]["user"] == {
        "id": str(user.id),
        "username": user.username,
    }


@pytest.mark.django_db
async def test_update_profile(test_context):
    context, organisation, workspace, user = test_context

    mutation = """
        mutation UpdateProfile($first_name: String!, $last_name: String!) {
            updateProfile(first_name: $first_name, last_name: $last_name) {
                id
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "first_name": "First Name",
            "last_name": "Test",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateProfile"] == {
        "id": str(user.id),
        "first_name": "First Name",
        "last_name": "Test",
    }


@pytest.mark.django_db
async def test_update_password(test_context):
    context, organisation, workspace, user = test_context

    user.set_password("old_password")
    await sync_to_async(user.save)()

    mutation = """
        mutation UpdatePassword($old_password: String!, $password: String!) {
            updatePassword(old_password: $old_password, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "old_password": "old_password",
            "password": "password",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updatePassword"] == {
        "id": str(user.id),
    }


@pytest.mark.django_db
async def test_update_password_wrong_password(test_context):
    context, organisation, workspace, user = test_context

    user.set_password("old_password")
    await sync_to_async(user.save)()

    mutation = """
        mutation UpdatePassword($old_password: String!, $password: String!) {
            updatePassword(old_password: $old_password, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "old_password": "old_password2",
            "password": "password",
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Old password does not match', locations=[SourceLocation(line=3, column=13)], path=['updatePassword'])]"
    )
    assert result.data is None


@pytest.mark.django_db
async def test_request_password_reset():
    User = get_user_model()

    user = await User.objects.acreate(username=generate_username())

    mutation = """
        mutation RequestPasswordReset($email: String!) {
            requestPasswordReset(email: $email) {
                success
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "email": user.username,
        },
    )

    assert result.errors is None
    assert result.data["requestPasswordReset"] == {"success": True}


@pytest.mark.django_db
async def test_request_password_reset_no_user():
    mutation = """
        mutation RequestPasswordReset($email: String!) {
            requestPasswordReset(email: $email) {
                success
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "email": "test2@example.com",
        },
    )

    assert result.errors is None
    assert result.data["requestPasswordReset"] == {"success": True}


@pytest.mark.django_db
async def test_reset_password(test_context):
    context, organisation, workspace, user = test_context

    token = default_token_generator.make_token(user)

    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={"token": token, "uid": str(user.pk), "password": "password"},
    )

    assert result.errors is None
    assert result.data["resetPassword"] == {
        "id": str(user.id),
    }


@pytest.mark.django_db
async def test_reset_password_invalid_token(test_context):
    context, organisation, workspace, user = test_context

    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": str(user.pk),
            "password": "password",
        },
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Token invalid', locations=[SourceLocation(line=3, column=13)], path=['resetPassword'])]"
    )
    assert result.data is None


@pytest.mark.django_db
async def test_reset_password_no_user():
    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": "85a3c968-15c4-4906-83ff-931a672c087f",
            "password": "password",
        },
    )

    assert (
        str(result.errors)
        == "[GraphQLError('User not found', locations=[SourceLocation(line=3, column=13)], path=['resetPassword'])]"
    )


@pytest.mark.django_db
async def test_complete_signup(test_context):
    context, organisation, workspace, user = test_context

    token = default_token_generator.make_token(user)

    mutation = """
        mutation CompleteSignup($token: String!, $uid: String!, $first_name: String!, $last_name: String!, $password: String!) {
            completeSignup(token: $token, uid: $uid, first_name: $first_name, last_name: $last_name, password: $password) {
                id
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": token,
            "uid": str(user.pk),
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
        },
    )

    assert result.errors is None
    assert result.data["completeSignup"] == {
        "id": str(user.id),
        "first_name": "First",
        "last_name": "Last",
    }


@pytest.mark.django_db
async def test_complete_signup_invalid_token(test_context):
    context, organisation, workspace, user = test_context

    mutation = """
        mutation CompleteSignup($token: String!, $uid: String!, $first_name: String!, $last_name: String!, $password: String!) {
            completeSignup(token: $token, uid: $uid, first_name: $first_name, last_name: $last_name, password: $password) {
                id
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": str(user.pk),
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
        },
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Token invalid', locations=[SourceLocation(line=3, column=13)], path=['completeSignup'])]"
    )
    assert result.data is None


@pytest.mark.django_db
async def test_complete_signup_no_user():
    mutation = """
        mutation CompleteSignup($token: String!, $uid: String!, $first_name: String!, $last_name: String!, $password: String!) {
            completeSignup(token: $token, uid: $uid, first_name: $first_name, last_name: $last_name, password: $password) {
                id
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": "85a3c968-15c4-4906-83ff-931a672c087f",
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
        },
    )

    assert (
        str(result.errors)
        == "[GraphQLError('User not found', locations=[SourceLocation(line=3, column=13)], path=['completeSignup'])]"
    )
    assert result.data is None


@pytest.mark.django_db
async def test_add_installation(test_context, mocker):
    mock = mocker.patch("api.mutations.base.Github")
    github_instance = MagicMock()
    owner = types.SimpleNamespace()
    owner.login = "default"
    repo = types.SimpleNamespace()
    repo.name = "repo1"
    repo.owner = owner
    github_instance.get_repos.return_value = [repo]
    mock.return_value = github_instance

    context, organisation, workspace, user = test_context

    mutation = """
        mutation AddInstallation($installationId: Int!) {
            addInstallation(installationId: $installationId) {
                success
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "installationId": 1234,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data == {"addInstallation": {"success": True}}


@pytest.mark.django_db
async def test_add_installation_no_repos(test_context, mocker):
    mock = mocker.patch("api.mutations.base.Github")
    github_instance = MagicMock()
    github_instance.get_repos.return_value = []
    mock.return_value = github_instance

    context, organisation, workspace, user = test_context

    mutation = """
        mutation AddInstallation($installationId: Int!) {
            addInstallation(installationId: $installationId) {
                success
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "installationId": 1234,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data == {"addInstallation": {"success": True}}
