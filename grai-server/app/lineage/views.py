from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from lineage.models import Edge, Node
from lineage.serializers import EdgeSerializer, NodeSerializer
from rest_framework import status
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt.authentication import JWTAuthentication
from workspaces.permissions import HasWorkspaceAPIKey

# Creating the user id automatically
# https://stackoverflow.com/questions/30582263/setting-user-id-automatically-on-post-in-django-rest


class NodeViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]

    permission_classes = [HasWorkspaceAPIKey | IsAuthenticated]

    serializer_class = NodeSerializer
    type = Node

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     pk = self.request.query_params.get("id")
    #     obj = queryset.filter(id=pk).first()#get_object_or_404(queryset, id=
    #     print(obj)
    #     return obj

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects

        supported_filters = ["is_active", "namespace", "name"]
        q_filter = Q()
        for filter_name in ["is_active", "namespace", "name"]:
            if condition := self.request.query_params.get(filter_name):
                q_filter &= Q(**{filter_name: condition})
        return self.type.objects.filter(q_filter)

    # def perform_destroy(self, instance):
    #     instance.is_active = False
    #     instance.save()

    # This is bugged.
    # def create(self, request):
    #     object, create = self.type.objects.update_or_create(**request.data)
    #     serializer = self.serializer_class(object)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.GET.get("workspace", None):
            data["workspace"] = request.GET.get("workspace")
        elif (
            request.user
            and not request.user.is_anonymous
            and request.user.memberships
            and request.user.memberships.first()
        ):
            data["workspace"] = str(request.user.memberships.first().workspace_id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class EdgeViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [HasAPIKey | HasWorkspaceAPIKey | IsAuthenticated]

    serializer_class = EdgeSerializer
    type = Edge

    # def get_object(self):
    #     return get_object_or_404(Edge, id=self.request.query_params.get("id"))

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects

        q_filter = Q()
        supported_filters = ["source", "destination", "is_active", "name", "namespace"]
        for filter_name in supported_filters:
            if condition := self.request.query_params.get(filter_name):
                q_filter &= Q(**{filter_name: condition})

        return self.type.objects.filter(q_filter)

    # def perform_destroy(self, instance):
    #     instance.is_active = False
    #     instance.save()

    # def create(self, request, *args, **kwargs):
    #     raise Exception(data, request.data['source'])
    #     return super().create(**data)
    #     object, create = self.type.objects.update_or_create(**request.data)
    #
    #     serializer = self.serializer_class(object)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.GET.get("workspace", None):
            data["workspace"] = request.GET.get("workspace")
        elif (
            request.user
            and not request.user.is_anonymous
            and request.user.memberships
            and request.user.memberships.first()
        ):
            data["workspace"] = str(request.user.memberships.first().workspace_id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
