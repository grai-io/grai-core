import pytest
from conftest import (
    generate_connection_name,
    generate_filter,
    generate_source,
    generate_workspace,
)

from api.schema import schema
from lineage.models import Filter, Source

##### FILTER #####


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


##### SOURCES #####


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_source(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CreateSource($workspaceId: ID!, $name: String!, $priority: Int!) {
            createSource(workspaceId: $workspaceId, name: $name, priority: $priority) {
                id
                name
                priority
                created_at
            }
        }
    """

    name = generate_connection_name()

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace.id),
            "name": name,
            "priority": 1,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["createSource"]["id"] != None
    assert result.data["createSource"]["name"] == name
    assert result.data["createSource"]["priority"] == 1


@pytest.mark.django_db
async def test_create_source_no_membership(test_context):
    context, organisation, workspace, user, membership = test_context

    workspace2 = await generate_workspace(organisation)

    mutation = """
        mutation CreateSource($workspaceId: ID!, $name: String!, $priority: Int!) {
            createSource(workspaceId: $workspaceId, name: $name, priority: $priority) {
                id
                name
                priority
                created_at
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "workspaceId": str(workspace2.id),
            "name": generate_connection_name(),
            "priority": 1,
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can\'t find workspace", locations=[SourceLocation(line=3, column=13)], path=[\'createSource\'])]"""
    )
    assert result.data is None


@pytest.mark.django_db
async def test_update_source(test_context):
    context, organisation, workspace, user, membership = test_context
    source = await generate_source(workspace)

    mutation = """
        mutation UpdateSource($id: ID!, $name: String!) {
            updateSource(id: $id, name: $name) {
                id
                name
                created_at
            }
        }
    """

    name = generate_connection_name()

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(source.id),
            "name": name,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateSource"]["id"] == str(source.id)
    assert result.data["updateSource"]["name"] == name


@pytest.mark.django_db
async def test_update_source_priority(test_context):
    context, organisation, workspace, user, membership = test_context
    source = await generate_source(workspace)

    mutation = """
        mutation UpdateSource($id: ID!, $priority: Int!) {
            updateSource(id: $id, priority: $priority) {
                id
                name
                priority
                created_at
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(source.id),
            "priority": 2,
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateSource"]["id"] == str(source.id)
    assert result.data["updateSource"]["priority"] == 2


@pytest.mark.django_db
async def test_update_source_no_membership(test_context):
    context, organisation, workspace, user, membership = test_context
    workspace2 = await generate_workspace(organisation)
    source = await generate_source(workspace2)

    mutation = """
        mutation UpdateSource($id: ID!, $name: String!) {
            updateSource(id: $id, name: $name) {
                id
                name
                created_at
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(source.id),
            "name": generate_connection_name(),
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == """[GraphQLError("Can't find source", locations=[SourceLocation(line=3, column=13)], path=['updateSource'])]"""
    )
    assert result.data is None


@pytest.mark.django_db
async def test_delete_source(test_context):
    context, organisation, workspace, user, membership = test_context
    source = await generate_source(workspace)

    mutation = """
        mutation DeleteSource($id: ID!) {
            deleteSource(id: $id) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "id": str(source.id),
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["deleteSource"]["id"] == str(source.id)

    with pytest.raises(Exception) as e_info:
        await Source.objects.aget(id=source.id)

    assert str(e_info.value) == "Source matching query does not exist."
