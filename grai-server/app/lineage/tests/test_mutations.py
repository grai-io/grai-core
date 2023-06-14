import pytest
from api.schema import schema
from api.tests.common import (
    generate_connection_name,
    generate_filter,
    generate_workspace,
    test_context,
    test_organisation,
    test_user,
    test_workspace,
)
from lineage.models import Filter


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_filter(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateFilter($workspaceId: ID!, $name: String!, $metadata: JSON!) {
            createFilter(workspaceId: $workspaceId, name: $name, metadata: $metadata) {
                id
                name
                metadata
                created_at
                updated_at
            }
        }
    """

    name = generate_connection_name()

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "name": name,
            "metadata": {},
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createFilter"]["id"] != None
    assert result.data["createFilter"]["name"] == name


@pytest.mark.django_db
async def test_create_filter_no_membership(test_context):
    context, organisation, workspace, user, membership = test_context

    workspace2 = await generate_workspace(organisation)

    mutation = """
        mutation CreateFilter($workspaceId: ID!, $name: String!, $metadata: JSON!) {
            createFilter(workspaceId: $workspaceId, name: $name, metadata: $metadata) {
                id
                name
                metadata
                created_at
                updated_at
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace2.id),
            "name": generate_connection_name(),
            "metadata": {},
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can\'t find workspace", locations=[SourceLocation(line=3, column=13)], path=[\'createFilter\'])]"""
    )
    assert result.data is None


@pytest.mark.django_db
async def test_update_filter(test_context):
    context, organisation, workspace, user, membership = test_context
    filter = await generate_filter(workspace, user)

    mutation = """
        mutation UpdateFilter($id: ID!, $name: String!, $metadata: JSON!) {
            updateFilter(id: $id, name: $name, metadata: $metadata) {
                id
                name
                metadata
                created_at
                updated_at
            }
        }
    """

    name = generate_connection_name()

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(filter.id),
            "name": name,
            "metadata": {},
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateFilter"]["id"] == str(filter.id)
    assert result.data["updateFilter"]["name"] == name


@pytest.mark.django_db
async def test_update_filter_no_membership(test_context):
    context, organisation, workspace, user, membership = test_context
    workspace2 = await generate_workspace(organisation)
    filter = await generate_filter(workspace2, user)

    mutation = """
        mutation UpdateFilter($id: ID!, $name: String!, $metadata: JSON!) {
            updateFilter(id: $id, name: $name, metadata: $metadata) {
                id
                name
                metadata
                created_at
                updated_at
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(filter.id),
            "name": generate_connection_name(),
            "metadata": {},
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can't find filter", locations=[SourceLocation(line=3, column=13)], path=['updateFilter'])]"""
    )
    assert result.data is None


@pytest.mark.django_db
async def test_delete_filter(test_context):
    context, organisation, workspace, user, membership = test_context
    filter = await generate_filter(workspace, user)

    mutation = """
        mutation DeleteFilter($id: ID!) {
            deleteFilter(id: $id) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(filter.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["deleteFilter"]["id"] == str(filter.id)

    with pytest.raises(Exception) as e_info:
        await Filter.objects.aget(id=filter.id)

    assert str(e_info.value) == "Filter matching query does not exist."
