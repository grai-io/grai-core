from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from workspaces.permissions import HasWorkspaceAPIKey


class HealthViewSet(viewsets.GenericViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [HasWorkspaceAPIKey | IsAuthenticated]

    def get_object(self):
        return
