import uuid

import pytest
from asgiref.sync import sync_to_async

from api.schema import schema
from workspaces.models import Workspace

from .common import (
    test_basic_context,
    test_context,
    test_organisation,
    test_user,
    test_workspace,
)


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_workspaces_no_login(test_basic_context):
    context = test_basic_context

    query = """
        query Workspaces {
            workspaces {
                id
                name
            }
        }
    """

    result = await schema.execute(
        query,
        context_value=context,
    )

    assert (
        str(result.errors)
        == "[GraphQLError('User is not authenticated', locations=[SourceLocation(line=3, column=13)],"
        " path=['workspaces'])]"
    )
    assert result.data is None


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_workspace_get(test_context):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($id: ID!) {
            workspace(id: $id) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "id": str(workspace.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"] == {
        "id": str(workspace.id),
        "name": workspace.name,
    }


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_workspace_name(test_context):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($name: String!, $organisationName: String!) {
            workspace(name: $name, organisationName: $organisationName) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "name": workspace.name,
            "organisationName": organisation.name,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["workspace"] == {
        "id": str(workspace.id),
        "name": workspace.name,
    }


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_workspace_none(test_context):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace {
            workspace {
                id
                name
            }
        }
    """

    result = await schema.execute(
        query,
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can't find workspace", locations=[SourceLocation(line=3, column=13)], path=['workspace'])]"""
    )


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_workspace_no_workspace(test_context):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspace($id: ID!) {
            workspace(id: $id) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "id": "85a3c968-15c4-4906-83ff-931a672c087f",
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can't find workspace", locations=[SourceLocation(line=3, column=13)], path=['workspace'])]"""
    )
    assert result.data is None


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_workspaces(test_context):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Workspaces {
            workspaces {
                id
                name
            }
        }
    """

    result = await schema.execute(query, context_value=context)

    assert result.errors is None
    assert result.data["workspaces"] == [{"id": str(workspace.id), "name": workspace.name}]


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_workspaces_no_membership(test_context):
    context, organisation, workspace, user, membership = test_context

    await Workspace.objects.acreate(name=str(uuid.uuid4()), organisation=organisation)

    query = """
        query Workspaces {
            workspaces {
                id
                name
            }
        }
    """

    result = await schema.execute(query, context_value=context)

    assert result.errors is None
    assert result.data["workspaces"] == [{"id": str(workspace.id), "name": workspace.name}]


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_profile(test_context):
    context, organisation, workspace, user, membership = test_context

    query = """
        query Profile {
            profile {
                id
                username
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(query, context_value=context)

    assert result.errors is None
    assert result.data["profile"] == {
        "id": str(user.id),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_profile_devices(test_context):
    context, organisation, workspace, user, membership = test_context

    token = "test123"

    device = await sync_to_async(user.staticdevice_set.create)()
    await sync_to_async(device.token_set.create)(token=token)

    query = """
        query Profile {
            profile {
                id
                devices {
                    data {
                        id
                        name
                    }
                }
            }
        }
    """

    result = await schema.execute(query, context_value=context)

    assert result.errors is None
    assert result.data["profile"] == {
        "id": str(user.id),
        "devices": {
            "data": [
                {
                    "id": str(device.persistent_id),
                    "name": device.name,
                }
            ]
        },
    }
