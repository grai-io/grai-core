from django_multitenant.utils import set_current_tenant

from rest_framework import permissions
from workspaces.models import Workspace, WorkspaceAPIKey


class BasePermission(permissions.BasePermission):
    def get_workspace(self, request, guess: bool = True):
        workspace = self.get_workspace_from_header(request)

        if workspace:
            return workspace

        if guess and request.user and not request.user.is_anonymous:
            if request.GET.get("workspace", None):
                id = request.GET.get("workspace")
                return self.get_workspace_from_id(request, id)

            if request.user.memberships and request.user.memberships.first():
                id = str(request.user.memberships.first().workspace_id)
                return self.get_workspace_from_id(request, id)

    def get_workspace_from_header(self, request):
        header = request.headers.get("Authorization")

        if header:
            [type, key] = header.split()
            # TODO: Consider handling Bearer token here
            if type == "Api-Key":
                try:
                    api_key = WorkspaceAPIKey.objects.get_from_key(key)
                    workspace = api_key.workspace
                    if workspace:
                        return workspace
                except WorkspaceAPIKey.DoesNotExist:
                    pass

    def get_workspace_from_id(self, request, id):
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
