from django.db.models import Q
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from common.permissions.multitenant import Multitenant
from lineage.models import Edge, Node, Source
from lineage.serializers import (
    EdgeSerializer,
    NodeSerializer,
    SourceEdgeSerializer,
    SourceNodeSerializer,
    SourceSerializer,
)
from rest_framework import status


class AuthenticatedViewSetMixin:
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]

    permission_classes = [Multitenant]


class HasSourceViewSetMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        source = Source.objects.get(pk=self.kwargs["source_pk"])

        instance.data_sources.remove(source)

        if not instance.data_sources.exists():
            self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class NodeViewSet(AuthenticatedViewSetMixin, ModelViewSet):
    serializer_class = NodeSerializer
    type = Node

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects

        q_filter = Q()
        query_params = self.request.query_params
        supported_filters = [
            "is_active",
            "namespace",
            "name",
            "display_name",
            "created_at",
            "updated_at",
            "source_name",
        ]
        starts_with_filters = ("metadata", "created_at", "updated_at")
        for filter_name, filter_value in query_params.items():
            if filter_name == "source_name":
                source = Source.objects.get(name=filter_value)
                q_filter &= Q(data_sources=source)
            elif filter_name in supported_filters or filter_name.startswith(starts_with_filters):
                q_filter &= Q(**{filter_name: filter_value})
        return self.type.objects.filter(q_filter)


class EdgeViewSet(AuthenticatedViewSetMixin, ModelViewSet):
    serializer_class = EdgeSerializer
    type = Edge

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects

        q_filter = Q()
        query_params = self.request.query_params
        supported_filters = {
            "source",
            "destination",
            "is_active",
            "name",
            "namespace",
            "display_name",
            "source_name",
        }
        starts_with_filters = ("metadata", "created_at", "updated_at")
        for filter_name, filter_value in query_params.items():
            if filter_name == "source_name":
                source = Source.objects.get(name=filter_value)
                q_filter &= Q(data_sources=source)
            elif filter_name in supported_filters or filter_name.startswith(starts_with_filters):
                q_filter &= Q(**{filter_name: filter_value})

        return self.type.objects.filter(q_filter)


class SourceViewSet(AuthenticatedViewSetMixin, ModelViewSet):
    serializer_class = SourceSerializer
    type = Source

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects

        q_filter = Q()
        query_params = self.request.query_params
        supported_filters = {"name"}
        starts_with_filters = ("metadata", "created_at", "updated_at")
        for filter_name, filter_value in query_params.items():
            if filter_name in supported_filters or filter_name.startswith(starts_with_filters):
                q_filter &= Q(**{filter_name: filter_value})

        return self.type.objects.filter(q_filter)


class SourceNodeViewSet(HasSourceViewSetMixin, NodeViewSet):
    serializer_class = SourceNodeSerializer

    def get_queryset(self):
        return super().get_queryset().filter(data_sources=self.kwargs["source_pk"])


class SourceEdgeViewSet(HasSourceViewSetMixin, EdgeViewSet):
    serializer_class = SourceEdgeSerializer

    def get_queryset(self):
        return super().get_queryset().filter(data_sources=self.kwargs["source_pk"])
