import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

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
async def test_login(test_basic_context):
    context = test_basic_context

    User = get_user_model()

    user = User(username=generate_username())
    user.set_password("password")
    await sync_to_async(user.save)()

    mutation = """
        mutation Login($username: String!, $password: String!) {
            login(username: $username, password: $password) {
                id
                username
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "username": user.username,
            "password": "password",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["login"] == {
        "id": str(user.id),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


@pytest.mark.django_db
async def test_login_bad_password(test_basic_context):
    context = test_basic_context

    User = get_user_model()

    user = User(username=generate_username())
    user.set_password("password")
    await sync_to_async(user.save)()

    mutation = """
        mutation Login($username: String!, $password: String!) {
            login(username: $username, password: $password) {
                id
                username
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "username": user.username,
            "password": "password2",
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Invalid credentials', locations=[SourceLocation(line=3, column=13)], path=['login'])]"
    )
    assert result.data is None


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_logout(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation Logout {
            logout
        }
    """

    result = await schema.execute(
        mutation,
        context_value=context,
    )

    assert result.errors is None
    assert result.data["logout"] == True


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_register(test_basic_context):
    context = test_basic_context

    mutation = """
        mutation Register($username: String!, $name: String!, $password: String!) {
            register(username: $username, name: $name, password: $password) {
                id
                username
                first_name
                last_name
            }
        }
    """

    username = generate_username()

    result = await schema.execute(
        mutation,
        variable_values={
            "username": username,
            "name": "Test Name Last",
            "password": "password",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["register"]["id"] is not None
    assert result.data["register"]["username"] == username
    assert result.data["register"]["first_name"] == "Test Name"
    assert result.data["register"]["last_name"] == "Last"


@pytest.mark.django_db
async def test_update_profile(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation UpdateProfile($first_name: String!, $last_name: String!) {
            updateProfile(first_name: $first_name, last_name: $last_name) {
                id
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "first_name": "First Name",
            "last_name": "Test",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updateProfile"] == {
        "id": str(user.id),
        "first_name": "First Name",
        "last_name": "Test",
    }


@pytest.mark.django_db
async def test_update_password(test_context):
    context, organisation, workspace, user, membership = test_context

    user.set_password("old_password")
    await sync_to_async(user.save)()

    mutation = """
        mutation UpdatePassword($old_password: String!, $password: String!) {
            updatePassword(old_password: $old_password, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "old_password": "old_password",
            "password": "password",
        },
        context_value=context,
    )

    assert result.errors is None
    assert result.data["updatePassword"] == {
        "id": str(user.id),
    }


@pytest.mark.django_db
async def test_update_password_wrong_password(test_context):
    context, organisation, workspace, user, membership = test_context

    user.set_password("old_password")
    await sync_to_async(user.save)()

    mutation = """
        mutation UpdatePassword($old_password: String!, $password: String!) {
            updatePassword(old_password: $old_password, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "old_password": "old_password2",
            "password": "password",
        },
        context_value=context,
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Old password does not match', locations=[SourceLocation(line=3, column=13)], path=['updatePassword'])]"
    )
    assert result.data is None


@pytest.mark.django_db
async def test_request_password_reset():
    User = get_user_model()

    user = await User.objects.acreate(username=generate_username())

    mutation = """
        mutation RequestPasswordReset($email: String!) {
            requestPasswordReset(email: $email) {
                success
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "email": user.username,
        },
    )

    assert result.errors is None
    assert result.data["requestPasswordReset"] == {"success": True}


@pytest.mark.django_db
async def test_request_password_reset_no_user():
    mutation = """
        mutation RequestPasswordReset($email: String!) {
            requestPasswordReset(email: $email) {
                success
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "email": "test2@example.com",
        },
    )

    assert result.errors is None
    assert result.data["requestPasswordReset"] == {"success": True}


@pytest.mark.django_db
async def test_reset_password(test_context):
    context, organisation, workspace, user, membership = test_context

    token = default_token_generator.make_token(user)

    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={"token": token, "uid": str(user.pk), "password": "password"},
    )

    assert result.errors is None
    assert result.data["resetPassword"] == {
        "id": str(user.id),
    }


@pytest.mark.django_db
async def test_reset_password_invalid_token(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": str(user.pk),
            "password": "password",
        },
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Token invalid', locations=[SourceLocation(line=3, column=13)], path=['resetPassword'])]"
    )
    assert result.data is None


@pytest.mark.django_db
async def test_reset_password_no_user():
    mutation = """
        mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
            resetPassword(token: $token, uid: $uid, password: $password) {
                id
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": "85a3c968-15c4-4906-83ff-931a672c087f",
            "password": "password",
        },
    )

    assert (
        str(result.errors)
        == "[GraphQLError('User not found', locations=[SourceLocation(line=3, column=13)], path=['resetPassword'])]"
    )


@pytest.mark.django_db
async def test_complete_signup(test_context):
    context, organisation, workspace, user, membership = test_context

    token = default_token_generator.make_token(user)

    mutation = """
        mutation CompleteSignup($token: String!, $uid: String!, $first_name: String!, $last_name: String!, $password: String!) {
            completeSignup(token: $token, uid: $uid, first_name: $first_name, last_name: $last_name, password: $password) {
                id
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": token,
            "uid": str(user.pk),
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
        },
    )

    assert result.errors is None
    assert result.data["completeSignup"] == {
        "id": str(user.id),
        "first_name": "First",
        "last_name": "Last",
    }


@pytest.mark.django_db
async def test_complete_signup_invalid_token(test_context):
    context, organisation, workspace, user, membership = test_context

    mutation = """
        mutation CompleteSignup($token: String!, $uid: String!, $first_name: String!, $last_name: String!, $password: String!) {
            completeSignup(token: $token, uid: $uid, first_name: $first_name, last_name: $last_name, password: $password) {
                id
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": str(user.pk),
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
        },
    )

    assert (
        str(result.errors)
        == "[GraphQLError('Token invalid', locations=[SourceLocation(line=3, column=13)], path=['completeSignup'])]"
    )
    assert result.data is None


@pytest.mark.django_db
async def test_complete_signup_no_user():
    mutation = """
        mutation CompleteSignup($token: String!, $uid: String!, $first_name: String!, $last_name: String!, $password: String!) {
            completeSignup(token: $token, uid: $uid, first_name: $first_name, last_name: $last_name, password: $password) {
                id
                first_name
                last_name
            }
        }
    """

    result = await schema.execute(
        mutation,
        variable_values={
            "token": "1234",
            "uid": "85a3c968-15c4-4906-83ff-931a672c087f",
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
        },
    )

    assert (
        str(result.errors)
        == "[GraphQLError('User not found', locations=[SourceLocation(line=3, column=13)], path=['completeSignup'])]"
    )
    assert result.data is None
