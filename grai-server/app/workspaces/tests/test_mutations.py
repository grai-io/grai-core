import uuid

import pytest
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


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_workspace(test_context):
    context, organisation, workspace, user = test_context

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
    context, organisation, workspace, user = test_context

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
