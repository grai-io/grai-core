import uuid

import pytest
from notifications.models import Alert

from api.schema import schema
from api.tests.common import (
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
async def test_create_alert(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateAlert($workspaceId: ID!, $name: String!, $channel: String!, $channel_metadata: JSON!, $triggers: JSON!, $is_active: Boolean) {
            createAlert(workspaceId: $workspaceId, name: $name, channel: $channel, channel_metadata: $channel_metadata, triggers: $triggers, is_active: $is_active) {
                id
                name
                channel
                channel_metadata
                triggers
                is_active
                created_at
            }
        }
    """

    name = str(uuid.uuid4())

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "name": name,
            "channel": "email",
            "channel_metadata": {},
            "triggers": {},
            "is_active": False,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createAlert"]["id"] != None
    assert result.data["createAlert"]["name"] == name


@pytest.mark.django_db
async def test_update_alert(test_context):
    context, organisation, workspace, user, membership = test_context

    alert = await Alert.objects.acreate(
        workspace=workspace,
        name=str(uuid.uuid4()),
        channel="email",
        channel_metadata={},
        triggers={},
        is_active=False,
    )

    mutation = """
        mutation UpdateAlert($id: ID!, $name: String!, $channel_metadata: JSON!, $triggers: JSON!, $is_active: Boolean) {
            updateAlert(id: $id, name: $name, channel_metadata: $channel_metadata, triggers: $triggers, is_active: $is_active) {
                id
                name
                channel
                channel_metadata
                triggers
                is_active
            }
        }
    """

    name = str(uuid.uuid4())

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(alert.id),
            "name": name,
            "channel_metadata": {},
            "triggers": {},
            "is_active": True,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateAlert"] == {
        "id": str(alert.id),
        "name": name,
        "channel": "email",
        "channel_metadata": {},
        "triggers": {},
        "is_active": True,
    }


@pytest.mark.django_db
async def test_delete_alert(test_context):
    context, organisation, workspace, user, membership = test_context

    alert = await Alert.objects.acreate(
        workspace=workspace,
        name=str(uuid.uuid4()),
        channel="email",
        channel_metadata={},
        triggers={},
        is_active=False,
    )

    mutation = """
        mutation DeleteAlert($id: ID!) {
            deleteAlert(id: $id) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(alert.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["deleteAlert"] == {
        "id": str(alert.id),
    }

    with pytest.raises(Exception) as e_info:
        await Alert.objects.aget(id=alert.id)

    assert str(e_info.value) == "Alert matching query does not exist."
