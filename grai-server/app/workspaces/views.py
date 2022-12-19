from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from workspaces.models import Workspace, Membership
from workspaces.serializers import WorkspaceSerializer, MembershipSerializer
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     pk = self.request.query_params.get("id")
    #     obj = queryset.filter(id=pk).first()#get_object_or_404(queryset, id=
    #     print(obj)
    #     return obj

    def get_queryset(self):
        queryset = self.type.objects

        supported_filters = ["name"]
        filters = (
            (filter_name, condition)
            for filter_name in supported_filters
            if (condition := self.request.query_params.get(filter_name))
        )
        for filter_name, condition in filters:
            queryset = queryset.filter(**{filter_name: condition})
        return queryset

    # def perform_destroy(self, instance):
    #     instance.is_active = False
    #     instance.save()

    # This is bugged.
    # def create(self, request):
    #     object, create = self.type.objects.update_or_create(**request.data)
    #     serializer = self.serializer_class(object)
    #     return Response(serializer.data)


class MembershipViewSet(ReadOnlyModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [HasWorkspaceAPIKey | IsAuthenticated]

    serializer_class = MembershipSerializer
    type = Membership

    # def get_object(self):
    #     return get_object_or_404(Edge, id=self.request.query_params.get("id"))

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
        # return Edge.objects.filter(is_active=True).order_by('-updated_at')

    # def perform_destroy(self, instance):
    #     instance.is_active = False
    #     instance.save()

    # def create(self, request):
    #     object, create = self.type.objects.update_or_create(**request.data)
    #     serializer = self.serializer_class(object)
    #     return Response(serializer.data)
