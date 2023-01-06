from decouple import config
from workspaces.models import (
    Workspace as WorkspaceModel,
    WorkspaceAPIKey,
    Membership as MembershipModel,
)
from api.types import (
    Connection,
    Workspace,
    KeyResult,
    Membership,
    User,
    BasicResult,
)
from connections.models import Connection as ConnectionModel
from strawberry.scalars import JSON
import strawberry
from strawberry.types import Info
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def createConnection(
        self,
        workspaceId: strawberry.ID,
        connectorId: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: JSON,
    ) -> Connection:
        connection = await ConnectionModel.objects.acreate(
            workspace_id=workspaceId,
            connector_id=connectorId,
            namespace=namespace,
            name=name,
            metadata=metadata,
            secrets=secrets,
        )

        return connection

    @strawberry.mutation
    async def updateConnection(
        self,
        id: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: JSON,
    ) -> Connection:
        connection = await ConnectionModel.objects.aget(pk=id)

        mergedSecrets = dict()
        mergedSecrets.update(connection.secrets)
        mergedSecrets.update(secrets)

        connection.namespace = namespace
        connection.name = name
        connection.metadata = metadata
        connection.secrets = mergedSecrets
        await connection.asave()

        return connection

    @strawberry.mutation
    async def createApiKey(
        self, info: Info, name: str, workspaceId: strawberry.ID
    ) -> KeyResult:
        user, _ = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        workspace = await WorkspaceModel.objects.aget(pk=workspaceId)

        api_key, key = await sync_to_async(WorkspaceAPIKey.objects.create_key)(
            name=name, created_by=user, workspace=workspace
        )

        return KeyResult(key=key, api_key=api_key)

    @strawberry.mutation
    async def updateWorkspace(
        self,
        id: strawberry.ID,
        name: str,
    ) -> Workspace:
        workspace = await WorkspaceModel.objects.aget(pk=id)
        workspace.name = name
        await workspace.asave()

        return workspace

    @strawberry.mutation
    async def createMembership(
        self,
        workspaceId: strawberry.ID,
        role: str,
        email: str,
    ) -> Membership:
        workspace = await WorkspaceModel.objects.aget(pk=workspaceId)

        UserModel = get_user_model()

        user = None

        try:
            user = await UserModel.objects.aget(username=email)
            email_template_name = "workspaces/invite_user_email.txt"
            subject = "Grai Workspace Invite"
        except UserModel.DoesNotExist:
            user = await UserModel.objects.acreate(username=email)
            email_template_name = "workspaces/new_user_email.txt"
            subject = "Grai Invite"

        membership = await MembershipModel.objects.acreate(
            role=role, user=user, workspace=workspace
        )

        c = {
            "email": user.username,
            "base_url": config("FRONTEND_URL", "http://localhost:3000"),
            "uid": user.pk,
            "user": user,
            "token": default_token_generator.make_token(user),
        }
        email_message = render_to_string(email_template_name, c)

        send_mail(
            subject,
            email_message,
            settings.EMAIL_FROM,
            [user.username],
            fail_silently=False,
        )

        return membership

    @strawberry.mutation
    async def updateProfile(self, info: Info, first_name: str, last_name: str) -> User:
        user, _ = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        user.first_name = first_name
        user.last_name = last_name

        await user.asave()

        return user

    @strawberry.mutation
    async def updatePassword(
        self, info: Info, old_password: str, password: str
    ) -> User:
        user, _ = await sync_to_async(JWTAuthentication().authenticate)(
            request=info.context.request
        )

        if not check_password(old_password, user.password):
            raise PermissionDenied("Old password does not match")

        user.set_password(password)
        await user.asave()

        return user

    @strawberry.mutation
    async def requestPasswordReset(self, email: str) -> BasicResult:
        UserModel = get_user_model()

        try:
            user = await UserModel.objects.filter(username=email).aget()

            subject = "Grai Password Reset"
            email_template_name = "auth/password_reset_email.txt"
            c = {
                "email": user.username,
                "base_url": config("FRONTEND_URL", "http://localhost:3000"),
                "uid": user.pk,
                "user": user,
                "token": default_token_generator.make_token(user),
            }
            email_message = render_to_string(email_template_name, c)

            send_mail(
                subject,
                email_message,
                settings.EMAIL_FROM,
                [user.username],
                fail_silently=False,
            )

        except UserModel.DoesNotExist:
            print("User not found")

        return BasicResult(success=True)

    @strawberry.mutation
    async def resetPassword(self, token: str, uid: str, password: str) -> User:
        UserModel = get_user_model()

        try:
            user = await UserModel.objects.aget(pk=uid)

            if not default_token_generator.check_token(user, token):
                raise Exception("Token invalid")

            user.set_password(password)
            await user.asave()
            return user

        except UserModel.DoesNotExist:
            raise Exception("User not found")

    @strawberry.mutation
    async def completeSignup(
        self, token: str, uid: str, first_name: str, last_name: str, password: str
    ) -> User:
        UserModel = get_user_model()

        try:
            user = await UserModel.objects.aget(pk=uid)

            if not default_token_generator.check_token(user, token):
                raise Exception("Token invalid")

            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            await user.asave()
            return user

        except UserModel.DoesNotExist:
            raise Exception("User not found")
