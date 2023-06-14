from typing import Optional
from django_multitenant.utils import set_current_tenant
from rest_framework import permissions
from workspaces.models import Workspace, WorkspaceAPIKey


class BasePermission(permissions.BasePermission):
    def get_workspace(self, request, guess: bool = True) -> Optional[Workspace]:
        workspace = self.get_workspace_from_header(request)

        if workspace:
            return workspace

        if guess and request.user and not request.user.is_anonymous:
            id = request.GET.get("workspace", request.data.get("workspace", None))

            if id:
                return self.get_workspace_from_id(request, id)

            membership = request.user.memberships.first()
            if membership:
                return Workspace(id=membership.workspace_id)

    def get_workspace_from_header(self, request) -> Optional[Workspace]:
        header = request.headers.get("Authorization")

        if header:
            split = header.split()
            if split[0] == "Api-Key":
                try:
                    api_key = WorkspaceAPIKey.objects.get_from_key(split[1])
                    workspace_id = api_key.workspace_id
                    if workspace_id:
                        return Workspace(id=workspace_id)
                except WorkspaceAPIKey.DoesNotExist:
                    pass

    def get_workspace_from_id(self, request, id) -> Workspace:
        try:
            return Workspace.objects.get(id=id, memberships__user_id=request.user.id)
        except Workspace.DoesNotExist:
            raise Exception("Can't find workspace")


class MultitenantWorkspaces(BasePermission):
    def has_permission(self, request, view):
        set_current_tenant(None)
        workspace = self.get_workspace(request, False)

        if workspace:
            set_current_tenant(workspace)

        return True


class Multitenant(BasePermission):
    def has_permission(self, request, view):
        set_current_tenant(None)
        workspace = self.get_workspace(request)

        if workspace:
            set_current_tenant(workspace)
            return True

        return False
