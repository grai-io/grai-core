import uuid

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

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
from workspaces.models import WorkspaceAPIKey


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_workspace(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateWorkspace($organisationName: String!, $name: String!) {
            createWorkspace(organisationName: $organisationName, name: $name) {
                id
                name
                organisation {
                    id
                    name
                }
            }
        }
    """

    organisationName = str(uuid.uuid4())

    result = await schema.execute(
        mutation,
        variable_values={
            "organisationName": organisationName,
            "name": "Test Workspace",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createWorkspace"]["id"] is not None
    assert result.data["createWorkspace"]["name"] == "Test Workspace"
    assert result.data["createWorkspace"]["organisation"]["id"] is not None
    assert result.data["createWorkspace"]["organisation"]["name"] == organisationName


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_workspace_existing_organisation(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateWorkspace($organisationId: ID!, $name: String!) {
            createWorkspace(organisationId: $organisationId, name: $name) {
                id
                name
                organisation {
                    id
                    name
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "organisationId": str(organisation.id),
            "name": "Test Workspace",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createWorkspace"]["id"] is not None
    assert result.data["createWorkspace"]["name"] == "Test Workspace"
    assert result.data["createWorkspace"]["organisation"]["id"] == str(organisation.id)
    assert result.data["createWorkspace"]["organisation"]["name"] == organisation.name


@pytest.mark.django_db
async def test_update_workspace(test_context):
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context

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
    context, organisation, workspace, user, membership = test_context
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
async def test_create_memberships(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateMemberships($workspaceId: ID!, $role: String!, $emails: [String!]!) {
            createMemberships(workspaceId: $workspaceId, role: $role, emails: $emails) {
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
            "emails": ["test@example.com", "test2@example.com"],
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createMemberships"][0]["role"] == "admin"
    assert result.data["createMemberships"][0]["user"]["username"] == "test@example.com"
    assert result.data["createMemberships"][1]["role"] == "admin"
    assert result.data["createMemberships"][1]["user"]["username"] == "test2@example.com"


@pytest.mark.django_db
async def test_update_membership(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation UpdateMembership($id: ID!, $role: String!, $is_active: Boolean!) {
            updateMembership(id: $id, role: $role, is_active: $is_active) {
                id
                role
                is_active
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(membership.id),
            "role": "admin",
            "is_active": False,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateMembership"]["id"] == str(membership.id)
    assert result.data["updateMembership"]["role"] == "admin"
    assert result.data["updateMembership"]["is_active"] is False


@pytest.mark.django_db
async def test_delete_membership(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation DeleteMembership($id: ID!) {
            deleteMembership(id: $id) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(membership.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["deleteMembership"]["id"] == str(membership.id)


@pytest.mark.django_db
async def test_create_api_key(test_context):
    context, organisation, workspace, user, membership = test_context

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
async def test_create_api_key_expiry_date(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateApiKey($workspaceId: ID!, $name: String!, $expiry_date: DateTime) {
            createApiKey(workspaceId: $workspaceId, name: $name, expiry_date: $expiry_date) {
                key
                api_key {
                    id
                    name
                    expiry_date
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "name": "test api key",
            "expiry_date": "2020-01-01",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createApiKey"]["key"] != None
    assert result.data["createApiKey"]["api_key"]["name"] == "test api key"
    assert result.data["createApiKey"]["api_key"]["expiry_date"] == "2020-01-01T00:00:00"


@pytest.mark.django_db
async def test_create_api_key_expiry_date_long(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateApiKey($workspaceId: ID!, $name: String!, $expiry_date: DateTime) {
            createApiKey(workspaceId: $workspaceId, name: $name, expiry_date: $expiry_date) {
                key
                api_key {
                    id
                    name
                    expiry_date
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "name": "test api key",
            "expiry_date": "2023-03-24T00:00:00.000+00:00",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createApiKey"]["key"] != None
    assert result.data["createApiKey"]["api_key"]["name"] == "test api key"
    assert result.data["createApiKey"]["api_key"]["expiry_date"] == "2023-03-24T00:00:00+00:00"


@pytest.mark.django_db
async def test_delete_api_key(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation DeleteApiKey($id: ID!) {
            deleteApiKey(id: $id) {
                id
                name
            }
        }
    """

    api_key, key = await sync_to_async(WorkspaceAPIKey.objects.create_key)(
        name="test api key", created_by=user, workspace=workspace
    )

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(api_key.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["deleteApiKey"]["id"] == str(api_key.id)
