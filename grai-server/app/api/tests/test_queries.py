from workspaces.models import Workspace, Membership
from api.schema import schema
import pytest
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model


class Info(object):
    pass


@pytest.fixture
async def test_info():
    User = get_user_model()

    workspace = await Workspace.objects.acreate(name="Test Workspace")
    user = await User.objects.acreate()
    await Membership.objects.acreate(user=user, workspace=workspace, role="admin")

    request = HttpRequest
    request.user = user

    info = Info()
    info.request = request

    return info, workspace, user


@pytest.mark.django_db
async def test_workspaces(test_info):
    info, workspace, user = test_info

    query = """
        query workspaces {
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
        query workspaces {
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
        query profile {
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


# @pytest.mark.asyncio
# async def test_mutation():
#     mutation = """
#         mutation TestMutation($title: String!, $author: String!) {
#             addBook(title: $title, author: $author) {
#                 title
#             }
#         }
#     """

#     resp = await schema.execute(
#         mutation,
#         variable_values={
#             "title": "The Little Prince",
#             "author": "Antoine de Saint-Exupéry",
#         },
#     )

#     assert resp.errors is None
#     assert resp.data["addBook"] == {
#         "title": "The Little Prince",
#     }
