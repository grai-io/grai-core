from typing import Optional
import strawberry
from asgiref.sync import sync_to_async
from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string
from strawberry.scalars import JSON
from strawberry.types import Info

from api.queries import IsAuthenticated
from api.types import BasicResult, Connection, KeyResult, Membership, User, Workspace
from connections.models import Connection as ConnectionModel
from connections.models import Run as RunModel
from connections.tasks import run_update_server
from workspaces.models import Membership as MembershipModel
from workspaces.models import Workspace as WorkspaceModel
from workspaces.models import WorkspaceAPIKey
from django.contrib.auth import authenticate, login

from .common import IsAuthenticated, get_user


async def get_workspace(info: Info, workspaceId: strawberry.ID):
    user = get_user(info)

    try:
        workspace = await WorkspaceModel.objects.aget(
            pk=workspaceId, memberships__user_id=user.id
        )
    except WorkspaceModel.DoesNotExist:
        raise Exception("Can't find workspace")

    return workspace


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def login(
        self,
        info: Info,
        username: str,
        password: str,
    ) -> User:
        user = authenticate(username=username, password=password)

        if user is None:
            raise Exception("Invalid credentials")

        login(info.context.request, user)

        return user

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createConnection(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        connectorId: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: Optional[JSON],
        schedules: Optional[JSON],
        is_active: Optional[bool],
    ) -> Connection:
        workspace = await get_workspace(info, workspaceId)

        connection = await ConnectionModel.objects.acreate(
            workspace=workspace,
            connector_id=connectorId,
            namespace=namespace,
            name=name,
            metadata=metadata,
            secrets=secrets,
            schedules=schedules,
            is_active=is_active if is_active is not None else True,
        )

        return connection

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateConnection(
        self,
        info: Info,
        id: strawberry.ID,
        namespace: str,
        name: str,
        metadata: JSON,
        secrets: Optional[JSON],
        schedules: Optional[JSON],
        is_active: Optional[bool],
    ) -> Connection:
        user = get_user(info)

        try:
            connection = await ConnectionModel.objects.aget(
                pk=id, workspace__memberships__user_id=user.id
            )
        except ConnectionModel.DoesNotExist:
            raise Exception("Can't find connection")

        mergedSecrets = dict()
        mergedSecrets.update(connection.secrets if connection.secrets else {})
        mergedSecrets.update(secrets if secrets else {})

        connection.namespace = namespace
        connection.name = name
        connection.metadata = metadata
        connection.secrets = mergedSecrets
        connection.schedules = schedules
        connection.is_active = is_active
        await sync_to_async(connection.save)()

        return connection

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def runConnection(
        self,
        info: Info,
        connectionId: strawberry.ID,
    ) -> Connection:
        user = get_user(info)

        try:
            connection = await sync_to_async(ConnectionModel.objects.get)(
                pk=connectionId, workspace__memberships__user_id=user.id
            )
        except ConnectionModel.DoesNotExist:
            raise Exception("Can't find connection")

        run = await sync_to_async(RunModel.objects.create)(
            connection=connection,
            workspace_id=connection.workspace_id,
            user=user,
            status="queued",
        )

        run_update_server.delay(run.id)

        return connection

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createApiKey(
        self, info: Info, name: str, workspaceId: strawberry.ID
    ) -> KeyResult:
        user = get_user(info)
        workspace = await get_workspace(info, workspaceId)

        api_key, key = await sync_to_async(WorkspaceAPIKey.objects.create_key)(
            name=name, created_by=user, workspace=workspace
        )

        return KeyResult(key=key, api_key=api_key)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateWorkspace(
        self,
        info: Info,
        id: strawberry.ID,
        name: str,
    ) -> Workspace:
        workspace = await get_workspace(info, id)

        workspace.name = name
        await sync_to_async(workspace.save)()

        return workspace

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createMembership(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        role: str,
        email: str,
    ) -> Membership:
        workspace = await get_workspace(info, workspaceId)

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

        membership = await sync_to_async(MembershipModel.objects.create)(
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

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateProfile(self, info: Info, first_name: str, last_name: str) -> User:
        user = get_user(info)

        user.first_name = first_name
        user.last_name = last_name

        await sync_to_async(user.save)()

        return user

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updatePassword(
        self, info: Info, old_password: str, password: str
    ) -> User:
        user = get_user(info)

        if not check_password(old_password, user.password):
            raise PermissionDenied("Old password does not match")

        user.set_password(password)
        await sync_to_async(user.save)()

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
            await sync_to_async(user.save)()
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
            await sync_to_async(user.save)()
            return user

        except UserModel.DoesNotExist:
            raise Exception("User not found")
