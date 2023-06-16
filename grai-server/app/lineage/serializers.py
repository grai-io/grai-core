from django.db.models import Q
from grai_schemas.v1.node import NodeNamedID

from rest_framework import serializers

from .models import Edge, Node, Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("created_at", "updated_at")


class ChildSourceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Source
        fields = ("id", "name")
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }


class NodeSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(required=False)
    data_sources = ChildSourceSerializer(many=True, required=False)

    class Meta:
        model = Node
        fields = (
            "id",
            "namespace",
            "name",
            "display_name",
            "metadata",
            "is_active",
            "data_sources",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        data_sources = validated_data.pop("data_sources", [])

        instance = super().create(validated_data)

        for data_source in data_sources:
            source = Source.objects.get(**data_source)
            source.nodes.add(instance)

        return instance

    def update(self, instance, validated_data):
        data_sources = validated_data.pop("data_sources", [])

        for data_source in data_sources:
            source = Source.objects.get(**data_source)
            source.nodes.add(instance)

        return super().update(instance, validated_data)


class EdgeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False)
    data_sources = ChildSourceSerializer(many=True, required=False)

    def get_data_sources(self, instance):
        return [item.name for item in instance.data_sources.all()]

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
            "data_sources",
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

    def create(self, validated_data):
        data_sources = validated_data.pop("data_sources", [])

        instance = super().create(validated_data)

        for data_source in data_sources:
            source = Source.objects.get(**data_source)
            source.edges.add(instance)

        return instance

    def update(self, instance, validated_data):
        data_sources = validated_data.pop("data_sources", [])

        for data_source in data_sources:
            source = Source.objects.get(**data_source)
            source.edges.add(instance)

        return super().update(instance, validated_data)


class SourceNodeSerializer(serializers.ModelSerializer):
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
        read_only_fields = (
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        node, updated = Node.objects.update_or_create(
            name=validated_data["name"],
            namespace=validated_data["namespace"],
            defaults=validated_data,
        )

        source = Source.objects.get(pk=self.context["view"].kwargs["source_pk"])

        source.nodes.add(node)

        return node

    def update(self, instance, validated_data):
        source = Source.objects.get(pk=self.context["view"].kwargs["source_pk"])

        source.nodes.add(instance)

        return super().update(instance, validated_data)


class SourceEdgeSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        source = Source.objects.get(pk=self.context["view"].kwargs["source_pk"])

        edge, updated = Edge.objects.update_or_create(
            source=validated_data["source"],
            destination=validated_data["destination"],
            defaults=validated_data,
        )

        source.edges.add(edge)

        return edge

    def update(self, instance, validated_data):
        source = Source.objects.get(pk=self.context["view"].kwargs["source_pk"])

        source.edges.add(instance)

        return super().update(instance, validated_data)
