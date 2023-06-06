from django.db.models import Q
from grai_schemas.v1.node import NodeNamedID

from rest_framework import serializers

from .models import Edge, Node, Source


class NodeSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(required=False)

    class Meta:
        model = Node
        fields = (
            "id",
            "namespace",
            "name",
            "display_name",
            "metadata",
            "is_active",
        )
        read_only_fields = ("created_at", "updated_at")


class EdgeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False)

    class Meta:
        model = Edge
        fields = (
            "id",
            "name",
            "display_name",
            "namespace",
            "metadata",
            "is_active",
            "source",
            "destination",
        )
        read_only_fields = ("created_at", "updated_at")

    def to_internal_value(self, data):
        if isinstance(source := data.get("source"), dict):
            source = NodeNamedID(**source)
        if isinstance(destination := data.get("destination"), dict):
            destination = NodeNamedID(**destination)

        match (source, destination):
            case (NodeNamedID(), str()):
                node = Node.objects.get(Q(name=source.name) & Q(namespace=source.namespace))
                data["source"] = node.id
            case (str(), NodeNamedID()):
                node = Node.objects.get(Q(name=destination.name) & Q(namespace=destination.namespace))
                data["destination"] = node.id
            case (NodeNamedID(), NodeNamedID()):
                q_filter = Q(name=source.name) & Q(namespace=source.namespace)
                q_filter |= Q(name=destination.name) & Q(namespace=destination.namespace)
                model_source, model_destination = Node.objects.filter(q_filter)
                data["source"] = model_source.id
                data["destination"] = model_destination.id
            case _:
                pass
        data = super().to_internal_value(data)
        return data


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("created_at", "updated_at")
