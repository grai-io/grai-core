from django.db.models import Q
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from common.permissions.multitenant import Multitenant
from lineage.models import Edge, Node
from lineage.serializers import EdgeSerializer, NodeSerializer
from workspaces.permissions import HasWorkspaceAPIKey

# Creating the user id automatically
# https://stackoverflow.com/questions/30582263/setting-user-id-automatically-on-post-in-django-rest


class NodeViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]

    permission_classes = [(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant]

    serializer_class = NodeSerializer
    type = Node

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects

        q_filter = Q()
        query_params = self.request.query_params
        supported_filters = ["is_active", "namespace", "name", "display_name", "created_at", "updated_at"]
        starts_with_filters = ("metadata", "created_at", "updated_at")
        for filter_name, filter_value in query_params.items():
            if filter_name in supported_filters or filter_name.startswith(starts_with_filters):
                q_filter &= Q(**{filter_name: filter_value})
        return self.type.objects.filter(q_filter)


class EdgeViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant]

    serializer_class = EdgeSerializer
    type = Edge

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects

        q_filter = Q()
        query_params = self.request.query_params
        supported_filters = {"source", "destination", "is_active", "name", "namespace", "display_name"}
        starts_with_filters = ("metadata", "created_at", "updated_at")
        for filter_name, filter_value in query_params.items():
            if filter_name in supported_filters or filter_name.startswith(starts_with_filters):
                q_filter &= Q(**{filter_name: filter_value})

        return self.type.objects.filter(q_filter)
