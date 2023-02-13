from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from common.permissions.multitenant import Multitenant, MultitenantWorkspaces
from workspaces.models import Membership, Workspace
from workspaces.permissions import HasWorkspaceAPIKey
from workspaces.serializers import MembershipSerializer, WorkspaceSerializer

# Creating the user id automatically
# https://stackoverflow.com/questions/30582263/setting-user-id-automatically-on-post-in-django-rest


class WorkspaceViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]

    permission_classes = [(HasWorkspaceAPIKey | IsAuthenticated) & MultitenantWorkspaces]

    serializer_class = WorkspaceSerializer
    type = Workspace

    def get_queryset(self):
        queryset = (
            self.type.objects.filter(memberships__user_id=self.request.user.id)
            if not self.request.user.is_anonymous
            else self.type.objects
        )

        supported_filters = ["name", "ref"]
        filters = (
            (filter_name, condition)
            for filter_name in supported_filters
            if (condition := self.request.query_params.get(filter_name))
        )
        for filter_name, condition in filters:
            if filter_name == "ref":
                split = condition.split("/")

                if len(split) == 1 or len(split) > 2:
                    raise Exception("Incorrect format, should be organisation/workspace")

                queryset = queryset.filter(name=split[1], organisation__name=split[0])
            else:
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
