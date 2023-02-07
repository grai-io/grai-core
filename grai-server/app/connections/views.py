from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt.authentication import JWTAuthentication

from common.permissions.multitenant import Multitenant
from connections.models import Connection, Connector, Run
from connections.serializers import (
    ConnectionSerializer,
    ConnectorSerializer,
    RunSerializer,
)
from workspaces.permissions import HasWorkspaceAPIKey

# Creating the user id automatically
# https://stackoverflow.com/questions/30582263/setting-user-id-automatically-on-post-in-django-rest


class ConnectionViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]

    permission_classes = [(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant]

    serializer_class = ConnectionSerializer
    type = Connection

    def get_queryset(self):
        queryset = self.type.objects

        supported_filters = ["is_active", "namespace", "name", "connector"]
        filters = (
            (filter_name, condition)
            for filter_name in supported_filters
            if (condition := self.request.query_params.get(filter_name))
        )
        for filter_name, condition in filters:
            queryset = queryset.filter(**{filter_name: condition})
        return queryset


class ConnectorViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [HasAPIKey | HasWorkspaceAPIKey | IsAuthenticated]

    serializer_class = ConnectorSerializer
    type = Connector

    def get_queryset(self):
        queryset = self.type.objects

        supported_filters = ["is_active", "name"]
        filters = (
            (filter_name, condition)
            for filter_name in supported_filters
            if (condition := self.request.query_params.get(filter_name))
        )
        for filter_name, condition in filters:
            queryset = queryset.filter(**{filter_name: condition})
        return queryset


class RunViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant]

    serializer_class = RunSerializer
    type = Run
