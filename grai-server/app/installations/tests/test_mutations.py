import types
from unittest.mock import MagicMock

import pytest
from django_multitenant.utils import set_current_tenant

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


@pytest.mark.django_db
async def test_add_installation(test_context, mocker):
    set_current_tenant(None)
    mock = mocker.patch("installations.mutations.Github")
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
        mutation AddInstallation($workspaceId: ID!, $installationId: Int!) {
            addInstallation(workspaceId: $workspaceId, installationId: $installationId) {
                success
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "installationId": 1234,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data == {"addInstallation": {"success": True}}


@pytest.mark.django_db
async def test_add_installation_no_repos(test_context, mocker):
    mock = mocker.patch("installations.mutations.Github")
    github_instance = MagicMock()
    github_instance.get_repos.return_value = []
    mock.return_value = github_instance

    context, organisation, workspace, user = test_context

    mutation = """
        mutation AddInstallation($workspaceId: ID!, $installationId: Int!) {
            addInstallation(workspaceId: $workspaceId, installationId: $installationId) {
                success
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "installationId": 1234,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data == {"addInstallation": {"success": True}}
