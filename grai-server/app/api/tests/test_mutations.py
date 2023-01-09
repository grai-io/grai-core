from connections.models import Connector, Connection
from workspaces.models import Workspace
from api.schema import schema
import pytest
from .common import test_info
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from asgiref.sync import sync_to_async


@pytest.mark.django_db
async def test_create_connection(test_info):
    info, workspace, user = test_info

    connector = await Connector.objects.acreate(name="Connector 1")

    mutation = """
        mutation CreateConnection($workspaceId: ID!, $connectorId: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            createConnection(workspaceId: $workspaceId, connectorId: $connectorId, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
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
            "secrets": None,
            "schedules": None,
            "is_active": False,
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["createConnection"]["id"] != None
    assert resp.data["createConnection"]["name"] == "test connection"


@pytest.mark.django_db
async def test_create_connection_no_membership(test_info):
    info, workspace, user = test_info

    workspace2 = await Workspace.objects.acreate(name="W2")

    connector = await Connector.objects.acreate(name="Connector 6")

    mutation = """
        mutation CreateConnection($workspaceId: ID!, $connectorId: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            createConnection(workspaceId: $workspaceId, connectorId: $connectorId, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
                id
                name
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace2.id),
            "connectorId": str(connector.id),
            "namespace": "default",
            "name": "test connection",
            "metadata": {},
            "secrets": None,
            "schedules": None,
            "is_active": False,
        },
        context_value=info,
    )

    assert (
        str(resp.errors)
        == """[GraphQLError("Can\'t find workspace", locations=[SourceLocation(line=3, column=13)], path=[\'createConnection\'])]"""
    )


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
        mutation UpdateConnection($id: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            updateConnection(id: $id, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
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
            "secrets": None,
            "schedules": None,
            "is_active": False,
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["updateConnection"] == {
        "id": str(connection.id),
        "name": "test connection3",
    }


@pytest.mark.django_db
async def test_update_connection_no_membership(test_info):
    info, workspace, user = test_info

    workspace2 = await Workspace.objects.acreate(name="W3")

    connector = await Connector.objects.acreate(name="Connector 7")
    connection = await Connection.objects.acreate(
        workspace=workspace2,
        connector=connector,
        namespace="default",
        name="test connection2",
        metadata={},
        secrets={},
    )

    mutation = """
        mutation UpdateConnection($id: ID!, $namespace: String!, $name: String!, $metadata: JSON!, $secrets: JSON, $schedules: JSON, $is_active: Boolean) {
            updateConnection(id: $id, namespace: $namespace, name: $name, metadata: $metadata, secrets: $secrets, schedules: $schedules, is_active: $is_active) {
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
            "secrets": None,
            "schedules": None,
            "is_active": False,
        },
        context_value=info,
    )

    assert (
        str(resp.errors)
        == """[GraphQLError("Can't find connection", locations=[SourceLocation(line=3, column=13)], path=['updateConnection'])]"""
    )


@pytest.mark.django_db
async def test_run_connection(test_info):
    info, workspace, user = test_info

    connector = await Connector.objects.acreate(name="Connector 3")
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name="test connection2",
        metadata={},
        secrets={},
    )

    mutation = """
        mutation RunConnection($connectionId: ID!) {
            runConnection(connectionId: $connectionId) {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "connectionId": str(connection.id),
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["runConnection"] == {
        "id": str(connection.id),
    }


@pytest.mark.django_db
async def test_run_connection_no_membership(test_info):
    info, workspace, user = test_info

    workspace2 = await Workspace.objects.acreate(name="W4")

    connector = await Connector.objects.acreate(name="Connector 8")
    connection = await Connection.objects.acreate(
        workspace=workspace2,
        connector=connector,
        namespace="default",
        name="test connection2",
        metadata={},
        secrets={},
    )

    mutation = """
        mutation RunConnection($connectionId: ID!) {
            runConnection(connectionId: $connectionId) {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "connectionId": str(connection.id),
        },
        context_value=info,
    )

    assert (
        str(resp.errors)
        == """[GraphQLError("Can't find connection", locations=[SourceLocation(line=3, column=13)], path=['runConnection'])]"""
    )


@pytest.mark.django_db
async def test_run_connection_postgres(test_info):
    info, workspace, user = test_info

    connector = await Connector.objects.acreate(name="Postgres")
    connection = await Connection.objects.acreate(
        workspace=workspace,
        connector=connector,
        namespace="default",
        name="test connection2",
        metadata={},
        secrets={},
    )

    mutation = """
        mutation RunConnection($connectionId: ID!) {
            runConnection(connectionId: $connectionId) {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "connectionId": str(connection.id),
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["runConnection"] == {
        "id": str(connection.id),
    }


@pytest.mark.django_db
async def test_create_api_key(test_info):
    info, workspace, user = test_info

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

    resp = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "name": "test api key",
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["createApiKey"]["key"] != None
    assert resp.data["createApiKey"]["api_key"]["name"] == "test api key"


@pytest.mark.django_db
async def test_update_workspace(test_info):
    info, workspace, user = test_info

    mutation = """
        mutation UpdateWorkspace($id: ID!, $name: String!) {
            updateWorkspace(id: $id, name: $name) {
                id
                name
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "id": str(workspace.id),
            "name": "Test Workspace 2",
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["updateWorkspace"] == {
        "id": str(workspace.id),
        "name": "Test Workspace 2",
    }


@pytest.mark.django_db
async def test_create_membership(test_info):
    info, workspace, user = test_info

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

    resp = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "role": "admin",
            "email": "test@example.com",
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["createMembership"]["role"] == "admin"
    assert resp.data["createMembership"]["user"]["username"] == "test@example.com"


@pytest.mark.django_db
async def test_create_membership_existing_user(test_info):
    info, workspace, user = test_info
    User = get_user_model()
    user = await User.objects.acreate(username="test2@grai.com")

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

    resp = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "role": "admin",
            "email": "test2@grai.com",
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["createMembership"]["role"] == "admin"
    assert resp.data["createMembership"]["user"] == {
        "id": str(user.id),
        "username": "test2@grai.com",
    }


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
async def test_update_password(test_info):
    info, workspace, user = test_info

    user.set_password("old_password")
    await sync_to_async(user.save)()

    mutation = """
        mutation UpdatePassword($old_password: String!, $password: String!) {
            updatePassword(old_password: $old_password, password: $password) {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "old_password": "old_password",
            "password": "password",
        },
        context_value=info,
    )

    assert resp.errors is None
    assert resp.data["updatePassword"] == {
        "id": str(user.id),
    }


@pytest.mark.django_db
async def test_update_password_wrong_password(test_info):
    info, workspace, user = test_info

    user.set_password("old_password")
    await sync_to_async(user.save)()

    mutation = """
        mutation UpdatePassword($old_password: String!, $password: String!) {
            updatePassword(old_password: $old_password, password: $password) {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "old_password": "old_password2",
            "password": "password",
        },
        context_value=info,
    )

    assert (
        str(resp.errors)
        == "[GraphQLError('Old password does not match', locations=[SourceLocation(line=3, column=13)], path=['updatePassword'])]"
    )


@pytest.mark.django_db
async def test_request_password_reset():
    User = get_user_model()

    user = await User.objects.acreate(username="test@grai.com")

    mutation = """
        mutation RequestPasswordReset($email: String!) {
            requestPasswordReset(email: $email) {
                success
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "email": user.username,
        },
    )

    assert resp.errors is None
    assert resp.data["requestPasswordReset"] == {"success": True}


@pytest.mark.django_db
async def test_request_password_reset_no_user():
    mutation = """
        mutation RequestPasswordReset($email: String!) {
            requestPasswordReset(email: $email) {
                success
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "email": "test2@example.com",
        },
    )

    assert resp.errors is None
    assert resp.data["requestPasswordReset"] == {"success": True}


@pytest.mark.django_db
async def test_reset_password(test_info):
    info, workspace, user = test_info

    token = default_token_generator.make_token(user)

    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={"token": token, "uid": str(user.pk), "password": "password"},
    )

    assert resp.errors is None
    assert resp.data["resetPassword"] == {
        "id": str(user.id),
    }


@pytest.mark.django_db
async def test_reset_password_invalid_token(test_info):
    info, workspace, user = test_info

    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": str(user.pk),
            "password": "password",
        },
    )

    assert (
        str(resp.errors)
        == "[GraphQLError('Token invalid', locations=[SourceLocation(line=3, column=13)], path=['resetPassword'])]"
    )


@pytest.mark.django_db
async def test_reset_password_no_user():
    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": "85a3c968-15c4-4906-83ff-931a672c087f",
            "password": "password",
        },
    )

    assert (
        str(resp.errors)
        == "[GraphQLError('User not found', locations=[SourceLocation(line=3, column=13)], path=['resetPassword'])]"
    )


@pytest.mark.django_db
async def test_complete_signup(test_info):
    info, workspace, user = test_info

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

    resp = await schema.execute(
        mutation,
        variable_values={
            "token": token,
            "uid": str(user.pk),
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
        },
    )

    assert resp.errors is None
    assert resp.data["completeSignup"] == {
        "id": str(user.id),
        "first_name": "First",
        "last_name": "Last",
    }


@pytest.mark.django_db
async def test_complete_signup_invalid_token(test_info):
    info, workspace, user = test_info

    mutation = """
        mutation CompleteSignup($token: String!, $uid: String!, $first_name: String!, $last_name: String!, $password: String!) {
            completeSignup(token: $token, uid: $uid, first_name: $first_name, last_name: $last_name, password: $password) {
                id
                first_name
                last_name
            }
        }
    """

    resp = await schema.execute(
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
        str(resp.errors)
        == "[GraphQLError('Token invalid', locations=[SourceLocation(line=3, column=13)], path=['completeSignup'])]"
    )


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

    resp = await schema.execute(
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
        str(resp.errors)
        == "[GraphQLError('User not found', locations=[SourceLocation(line=3, column=13)], path=['completeSignup'])]"
    )
