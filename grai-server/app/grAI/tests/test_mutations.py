import pytest

from api.schema import schema


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_fetch_or_create_chats(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation FetchChats($workspaceId: ID!) {
            fetchOrCreateChats(workspaceId: $workspaceId) {
                data {
                  id
                  messages {
                    data
                    {
                      id
                      message
                    }
                  }
                }
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
        },
        context_value=context,
    )

    assert result.errors is None
    # assert result.data["fetchOrCreateChats"]["data"]["id"] is not None
    # assert result.data["createWorkspace"]["name"] == "Test Workspace"
    # assert result.data["createWorkspace"]["organisation"]["id"] is not None
    # assert result.data["createWorkspace"]["organisation"]["name"] == organisationName


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_chat(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateChat($workspaceId: ID!) {
            createChat(workspaceId: $workspaceId) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createChat"]["id"] is not None
