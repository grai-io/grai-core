import pytest

from api.schema import schema
from workspaces.models import Workspace

from .common import test_info


@pytest.mark.django_db
async def test_workspace(test_info):
    info, workspace, user = test_info

    query = """
        query Workspace($pk: ID!) {
            workspace(pk: $pk) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "pk": str(workspace.id),
        },
        context_value=info,
    )

    assert result.errors is None
    assert result.data["workspace"] == {
        "id": str(workspace.id),
        "name": "Test Workspace",
    }


@pytest.mark.django_db
async def test_workspace_no_workspace(test_info):
    info, workspace, user = test_info

    query = """
        query Workspace($pk: ID!) {
            workspace(pk: $pk) {
                id
                name
            }
        }
    """

    result = await schema.execute(
        query,
        variable_values={
            "pk": "85a3c968-15c4-4906-83ff-931a672c087f",
        },
        context_value=info,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can't find workspace", locations=[SourceLocation(line=3, column=13)], path=['workspace'])]"""
    )


@pytest.mark.django_db
async def test_workspaces(test_info):
    info, workspace, user = test_info

    query = """
        query Workspaces {
            workspaces {
                id
                name
            }
        }
    """

    result = await schema.execute(query, context_value=info)

    assert result.errors is None
    assert result.data["workspaces"] == [
        {
            "id": str(workspace.id),
            "name": "Test Workspace",
        }
    ]


@pytest.mark.django_db
async def test_workspaces_no_membership(test_info):
    info, workspace, user = test_info

    await Workspace.objects.acreate(name="Test Workspace2")

    query = """
        query Workspaces {
            workspaces {
                id
                name
            }
        }
    """

    result = await schema.execute(query, context_value=info)

    assert result.errors is None
    assert result.data["workspaces"] == [
        {
            "id": str(workspace.id),
            "name": "Test Workspace",
        }
    ]


@pytest.mark.django_db
async def test_profile(test_info):
    info, workspace, user = test_info

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

    result = await schema.execute(query, context_value=info)

    assert result.errors is None
    assert result.data["profile"] == {
        "id": str(user.id),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
