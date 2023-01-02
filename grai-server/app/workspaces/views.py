from common.permissions.multitenant import Multitenant
from workspaces.models import Workspace, Membership
from workspaces.serializers import WorkspaceSerializer, MembershipSerializer
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from workspaces.permissions import HasWorkspaceAPIKey

# Creating the user id automatically
# https://stackoverflow.com/questions/30582263/setting-user-id-automatically-on-post-in-django-rest


class WorkspaceViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]

    permission_classes = [HasWorkspaceAPIKey | IsAuthenticated]

    serializer_class = WorkspaceSerializer
    type = Workspace

    def get_queryset(self):
        queryset = self.type.objects.filter(memberships__user_id=self.request.user.id)

        supported_filters = ["name"]
        filters = (
            (filter_name, condition)
            for filter_name in supported_filters
            if (condition := self.request.query_params.get(filter_name))
        )
        for filter_name, condition in filters:
            queryset = queryset.filter(**{filter_name: condition})
        return queryset


class MembershipViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant]

    serializer_class = MembershipSerializer
    type = Membership

    def get_queryset(self):
        queryset = self.type.objects

        supported_filters = ["is_active", "name", "user", "workspace", "role"]
        filters = (
            (filter_name, condition)
            for filter_name in supported_filters
            if (condition := self.request.query_params.get(filter_name))
        )
        for filter_name, condition in filters:
            queryset = queryset.filter(**{filter_name: condition})
        return queryset
