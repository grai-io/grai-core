from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from urllib.parse import urlparse
import re
from typing import Optional
from workspaces.models import Workspace, Membership
from users.models import User


class InvalidPathError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


class WorkspacePathAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        user = scope.get("user", None)
        if user is None or not user.is_authenticated:
            raise PermissionDeniedError("You must be logged in to access this resource.")

        workspace_id = self.extract_pattern(scope["path"])
        if workspace_id is None:
            raise InvalidPathError("You must specify a workspace in the path.")

        has_access = await self.user_has_workspace_access(user, workspace_id)
        if not has_access:
            raise PermissionDeniedError("You do not have permission to access this resource.")

        scope.setdefault("metadata", {})
        scope["metadata"]["workspace_id"] = workspace_id
        return await super().__call__(scope, receive, send)

    @staticmethod
    def extract_pattern(path) -> Optional[str]:
        workspace = re.search(r"/chat/([^/]+)/", path)
        return workspace.group(1) if workspace is not None else None

    @database_sync_to_async
    def user_has_workspace_access(self, user: User, workspace: str) -> bool:
        return Membership.objects.filter(user=user.id, workspace=workspace, is_active=True).exists()
