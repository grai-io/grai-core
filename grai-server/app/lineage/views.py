from django.db.models import Q
from django.db.models.query import prefetch_related_objects
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_multitenant.utils import get_current_tenant

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
            instance.is_active = False
            instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class NodeViewSet(AuthenticatedViewSetMixin, ModelViewSet):
    serializer_class = NodeSerializer
    type = Node

    def get_queryset(self):
        return self._get_queryset().all()

    def _get_queryset(self):
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
        starts_with_filters = ("metadata", "created_at", "updated_at", "data_sources")
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
        return self._get_queryset().all()

    def _get_queryset(self):
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


class UpsertModelMixin:
    def create(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        try:
            instance = self.get_upsert_object(request)

        except self.type.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=False)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance,
            # and then re-prefetch related objects
            instance._prefetched_objects_cache = {}  # pragma: no cover
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)  # pragma: no cover

        return Response(serializer.data)


class SourceViewSet(AuthenticatedViewSetMixin, ModelViewSet):
    serializer_class = SourceSerializer
    type = Source

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects.all()

        q_filter = Q()
        query_params = self.request.query_params
        supported_filters = {"name"}
        starts_with_filters = ("created_at", "updated_at")
        for filter_name, filter_value in query_params.items():
            if filter_name in supported_filters or filter_name.startswith(starts_with_filters):
                q_filter &= Q(**{filter_name: filter_value})

        return self.type.objects.filter(q_filter).all()


class SourceNodeViewSet(HasSourceViewSetMixin, UpsertModelMixin, NodeViewSet):
    serializer_class = SourceNodeSerializer

    def get_queryset(self):
        return super()._get_queryset().filter(data_sources=self.kwargs["source_pk"]).all()

    def get_upsert_object(self, request):
        return self.type.objects.get(name=request.data["name"], namespace=request.data["namespace"])


class SourceEdgeViewSet(HasSourceViewSetMixin, UpsertModelMixin, EdgeViewSet):
    serializer_class = SourceEdgeSerializer

    def get_queryset(self):
        return super()._get_queryset().filter(data_sources=self.kwargs["source_pk"]).all()

    def get_upsert_object(self, request):
        return self.type.objects.get(name=request.data["name"], namespace=request.data["namespace"])
