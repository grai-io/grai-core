import datetime
from typing import List, Optional

import strawberry
from asgiref.sync import async_to_sync, sync_to_async
from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.template.loader import render_to_string
from psycopg2 import errorcodes as pg_errorcodes
from strawberry.types import Info

from api.common import IsAuthenticated, aget_workspace, get_user, get_workspace
from api.types import KeyResult, Membership, Workspace, WorkspaceAPIKey
from api.validation import validate_no_slash
from lineage.extended_graph_cache import ExtendedGraphCache
from lineage.models import Edge, Node
from workspaces.models import Membership as MembershipModel
from workspaces.models import Organisation as OrganisationModel
from workspaces.models import Workspace as WorkspaceModel
from workspaces.models import WorkspaceAPIKey as WorkspaceAPIKeyModel

from .sample_data import SampleData


def handle_unique_error(exc: IntegrityError, message: str):
    if exc.__cause__.pgcode == pg_errorcodes.UNIQUE_VIOLATION:
        raise ValueError(message)

    raise exc


def create_single_membership(workspace: WorkspaceModel, email: str, role: str) -> MembershipModel:
    UserModel = get_user_model()

    user = None

    user, created = UserModel.objects.get_or_create(username=email)

    email_template_name = "workspaces/new_user_email.txt" if created else "workspaces/invite_user_email.txt"
    subject = "Grai Invite" if created else "Grai Workspace Invite"

    membership = MembershipModel.objects.create(role=role, user=user, workspace=workspace)

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


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createWorkspace(
        self,
        info: Info,
        name: str,
        sample_data: Optional[bool] = False,
        organisationId: Optional[strawberry.ID] = strawberry.UNSET,
        organisationName: Optional[str] = strawberry.UNSET,
    ) -> Workspace:
        @transaction.atomic
        def _create_workspace(
            info: Info,
            name: str,
            sample_data: bool,
            organisationId: str,
            organisationName: str,
        ) -> Workspace:
            user = get_user(info)

            validate_no_slash(name, "Workspace name")
            validate_no_slash(organisationName, "Organisation name")

            try:
                organisation = (
                    OrganisationModel.objects.get(id=organisationId)
                    if organisationId
                    else OrganisationModel.objects.create(name=organisationName)
                )
            except IntegrityError as exc:
                handle_unique_error(
                    exc,
                    "Organisation name already exists, choose another one, or contact your administrator",
                )

            try:
                workspace = WorkspaceModel.objects.create(organisation=organisation, name=name)
            except IntegrityError as exc:
                handle_unique_error(exc, "Workspace name already exists, choose another one")

            MembershipModel.objects.create(user=user, workspace=workspace, role="admin")

            if sample_data:
                generator = SampleData(workspace)
                async_to_sync(generator.generate)()

            return workspace

        return await sync_to_async(_create_workspace)(info, name, sample_data, organisationId, organisationName)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateWorkspace(
        self,
        info: Info,
        id: strawberry.ID,
        name: str,
    ) -> Workspace:
        validate_no_slash(name, "Workspace name")

        workspace = await aget_workspace(info, id)

        workspace.name = name
        await sync_to_async(workspace.save)()

        return workspace

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def clearWorkspace(
        self,
        info: Info,
        id: strawberry.ID,
    ) -> Workspace:
        def _clearWorkspace(workspace: WorkspaceModel):
            edges = Edge.objects.filter(workspace=workspace)

            if edges.exists():
                edges._raw_delete(edges.db)

            nodes = Node.objects.filter(workspace=workspace)

            if nodes.exists():
                nodes._raw_delete(nodes.db)

            cache = ExtendedGraphCache(workspace)
            cache.clear_cache()

        workspace = await aget_workspace(info, id)

        await sync_to_async(_clearWorkspace)(workspace)

        return workspace

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def loadWorkspaceSampleData(
        self,
        info: Info,
        id: strawberry.ID,
    ) -> Workspace:
        @transaction.atomic
        def _load_workspace_sample_data(info: Info, workspace: WorkspaceModel) -> Workspace:
            generator = SampleData(workspace)
            async_to_sync(generator.generate)()

            return workspace

        workspace = await aget_workspace(info, id)

        return await sync_to_async(_load_workspace_sample_data)(info, workspace)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createMembership(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        role: str,
        email: str,
    ) -> Membership:
        @transaction.atomic
        def _create_membership(info: Info, workspaceId: strawberry.ID, role: str, email: str) -> Membership:
            workspace = get_workspace(info, workspaceId)

            return create_single_membership(workspace, email, role)

        return await sync_to_async(_create_membership)(info, workspaceId, role, email)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createMemberships(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        role: str,
        emails: List[str],
    ) -> List[Membership]:
        @transaction.atomic
        def _create_memberships(
            info: Info,
            workspaceId: strawberry.ID,
            role: str,
            emails: List[str],
        ) -> List[Membership]:
            workspace = get_workspace(info, workspaceId)

            return [create_single_membership(workspace, email, role) for email in emails]

        return await sync_to_async(_create_memberships)(info, workspaceId, role, emails)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def updateMembership(
        self,
        id: strawberry.ID,
        role: str,
        is_active: bool,
    ) -> Membership:
        membership = await MembershipModel.objects.aget(id=id)

        membership.role = role
        membership.is_active = is_active

        await sync_to_async(membership.save)()

        return membership

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def deleteMembership(
        self,
        id: strawberry.ID,
    ) -> Membership:
        membership = await MembershipModel.objects.aget(id=id)

        await sync_to_async(membership.delete)()

        membership.id = id

        return membership

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def createApiKey(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        name: str,
        expiry_date: Optional[datetime.datetime] = None,
    ) -> KeyResult:
        user = get_user(info)
        workspace = await aget_workspace(info, workspaceId)

        api_key, key = await sync_to_async(WorkspaceAPIKeyModel.objects.create_key)(
            name=name,
            created_by=user,
            workspace=workspace,
            expiry_date=expiry_date,
        )

        return KeyResult(key=key, api_key=api_key)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def deleteApiKey(self, id: strawberry.ID) -> WorkspaceAPIKey:
        api_key = await WorkspaceAPIKeyModel.objects.aget(id=id)

        await sync_to_async(api_key.delete)()

        api_key.id = id

        return api_key
