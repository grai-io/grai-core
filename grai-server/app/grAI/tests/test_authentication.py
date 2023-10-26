import uuid

import pytest

from channels.middleware import BaseMiddleware
from channels.testing import WebsocketCommunicator
from grAI.authentication import (
    InvalidPathError,
    PermissionDeniedError,
    WorkspacePathAuthMiddleware,
)


@pytest.mark.django_db(transaction=True)
class TestWorkspacePathAuthMiddleware:
    @pytest.mark.asyncio
    async def test_workspace_path_auth_middleware(self, user, workspace, membership, simple_application):
        communicator = WebsocketCommunicator(WorkspacePathAuthMiddleware(simple_application), f"/chat/{workspace.id}/")
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        assert connected
        assert "metadata" in communicator.scope
        assert communicator.scope["metadata"]["workspace_id"] == str(workspace.id)
        assert communicator.scope["metadata"]["membership"] == membership

    @pytest.mark.asyncio
    async def test_workspace_path_auth_middleware_no_user(self, workspace, simple_application):
        communicator = WebsocketCommunicator(WorkspacePathAuthMiddleware(simple_application), f"/chat/{workspace.id}/")
        with pytest.raises(PermissionDeniedError):  # Update with your actual exception
            await communicator.connect()

    @pytest.mark.asyncio
    async def test_workspace_path_auth_middleware_invalid_path(self, user, simple_application):
        communicator = WebsocketCommunicator(WorkspacePathAuthMiddleware(simple_application), "/invalidpath/")
        communicator.scope["user"] = user
        with pytest.raises(InvalidPathError):  # Update with your actual exception
            await communicator.connect()

    @pytest.mark.asyncio
    async def test_workspace_path_auth_middleware_no_membership(self, user, workspace, simple_application):
        communicator = WebsocketCommunicator(WorkspacePathAuthMiddleware(simple_application), f"/chat/{workspace.id}/")
        communicator.scope["user"] = user
        with pytest.raises(PermissionDeniedError):  # Update with your actual exception
            await communicator.connect()
