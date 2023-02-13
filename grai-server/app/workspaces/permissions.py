from rest_framework_api_key.permissions import BaseHasAPIKey

from .models import WorkspaceAPIKey


class HasWorkspaceAPIKey(BaseHasAPIKey):
    model = WorkspaceAPIKey
