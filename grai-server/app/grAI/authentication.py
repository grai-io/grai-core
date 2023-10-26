import re
from typing import Optional
from urllib.parse import urlparse

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from users.models import User
from workspaces.models import Membership, Workspace


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

        membership = await self.get_membership(user, workspace_id)
        if membership is None:
            raise PermissionDeniedError("You do not have permission to access this resource.")

        scope.setdefault("metadata", {})
        scope["metadata"]["workspace_id"] = workspace_id
        scope["metadata"]["membership"] = membership
        return await super().__call__(scope, receive, send)

    @staticmethod
    def extract_pattern(path) -> Optional[str]:
        workspace = re.search(r"/chat/([^/]+)/", path)
        return workspace.group(1) if workspace is not None else None

    @database_sync_to_async
    def get_membership(self, user: User, workspace: str) -> Membership | None:
        membership = Membership.objects.filter(user=user.id, workspace=workspace, is_active=True).all()
        return membership[0] if len(membership) > 0 else None
