from django.db.models import Q
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from common.permissions.multitenant import Multitenant
from lineage.models import Edge, Node
from lineage.serializers import EdgeSerializer, NodeSerializer
from workspaces.permissions import HasWorkspaceAPIKey


class NodeViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]

    permission_classes = [Multitenant]

    serializer_class = NodeSerializer
    type = Node

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects.all()

        q_filter = Q()
        query_params = self.request.query_params
        supported_filters = [
            "is_active",
            "namespace",
            "name",
            "display_name",
            "created_at",
            "updated_at",
        ]
        starts_with_filters = ("metadata", "created_at", "updated_at")
        for filter_name, filter_value in query_params.items():
            if filter_name in supported_filters or filter_name.startswith(starts_with_filters):
                q_filter &= Q(**{filter_name: filter_value})
        return self.type.objects.filter(q_filter).all()


class EdgeViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]
    permission_classes = [Multitenant]

    serializer_class = EdgeSerializer
    type = Edge

    # def create(self, request, *args, **kwargs):
    #     source = parse_named_node(request.data["source"])
    #     destination = parse_named_node(request.data["destination"])
    #
    #     if source is not None or destination is not None:
    #         if hasattr(request.data, "_mutable"):
    #             request.data._mutable = True
    #
    #     match (source, destination):
    #         case (NodeNamedID(), None):
    #             node = Node.objects.get(Q(name=source.name) & Q(namespace=source.namespace))
    #             request.data["source"] = node.id
    #         case (None, NodeNamedID()):
    #             node = Node.objects.get(Q(name=destination.name) & Q(namespace=destination.namespace))
    #             request.data["destination"] = node.id
    #         case (NodeNamedID(), NodeNamedID()):
    #             q_filter = Q(name=source.name) & Q(namespace=source.namespace)
    #             q_filter |= Q(name=destination.name) & Q(namespace=destination.namespace)
    #             model_source, model_destination = Node.objects.filter(q_filter)
    #             request.data["source"] = model_source.id
    #             request.data["destination"] = model_destination.id
    #         case _:
    #             pass
    #
    #     return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return self.type.objects.all()

        q_filter = Q()
        query_params = self.request.query_params
        supported_filters = {
            "source",
            "destination",
            "is_active",
            "name",
            "namespace",
            "display_name",
        }
        starts_with_filters = ("metadata", "created_at", "updated_at")
        for filter_name, filter_value in query_params.items():
            if filter_name in supported_filters or filter_name.startswith(starts_with_filters):
                q_filter &= Q(**{filter_name: filter_value})

        return self.type.objects.filter(q_filter).all()
