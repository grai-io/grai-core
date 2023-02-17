from typing import Optional

import strawberry
from asgiref.sync import sync_to_async
from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from strawberry.types import Info

from api.common import IsAuthenticated, get_user, get_workspace
from api.types import KeyResult, Membership, Workspace
from workspaces.models import Membership as MembershipModel
from workspaces.models import Organisation as OrganisationModel
from workspaces.models import Workspace as WorkspaceModel
from workspaces.models import WorkspaceAPIKey


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createWorkspace(
        self,
        info: Info,
        name: str,
        organisationId: Optional[strawberry.ID] = None,
        organisationName: Optional[str] = None,
    ) -> Workspace:
        user = get_user(info)

        organisation = (
            await OrganisationModel.objects.aget(id=organisationId)
            if organisationId
            else await OrganisationModel.objects.acreate(name=organisationName)
        )
        workspace = await WorkspaceModel.objects.acreate(organisation=organisation, name=name)
        await MembershipModel.objects.acreate(user=user, workspace=workspace, role="admin")

        return workspace

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createApiKey(self, info: Info, name: str, workspaceId: strawberry.ID) -> KeyResult:
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

        membership = await sync_to_async(MembershipModel.objects.create)(role=role, user=user, workspace=workspace)

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
