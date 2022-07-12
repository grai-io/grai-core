from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from rest_framework.viewsets import ModelViewSet
from lineage.models import Node, Edge
from lineage.serializers import NodeSerializer, EdgeSerializer


# Creating the user id automatically
# https://stackoverflow.com/questions/30582263/setting-user-id-automatically-on-post-in-django-rest

class NodeViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [HasAPIKey | IsAuthenticated]

    serializer_class = NodeSerializer

    def get_object(self):
        return get_object_or_404(Node, id=self.request.query_params.get("id"))

    def get_queryset(self):
        queryset = Node.objects

        supported_filters = ['is_active', 'namespace', 'name']
        filters = ((filter_name, condition) for filter_name in supported_filters
                   if (condition := self.request.query_params.get(filter_name)))
        for filter_name, condition in filters:
            queryset = queryset.filter(**{filter_name: condition})
        return queryset

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class EdgeViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [HasAPIKey | IsAuthenticated]

    serializer_class = EdgeSerializer

    def get_object(self):
        return get_object_or_404(Edge, id=self.request.query_params.get("id"))

    def get_queryset(self):
        return Edge.objects.filter(is_active=True).order_by('-updated_at')

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

