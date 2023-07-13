from functools import cached_property
from typing import Optional

from django.db.models import Q
from grai_schemas.utilities import merge
from grai_schemas.v1.node import NodeNamedID
from rest_framework.fields import JSONField

from rest_framework import serializers

from .models import Edge, Node, Source


def merge_tags(a: Optional[list], b: Optional[list]) -> list:
    a_tag = set(a) if a is not None else set()
    b_tag = set(b) if b is not None else set()
    return list(a_tag.union(b_tag))


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


class SourceParentMixin:
    def _get_source(self, data) -> Source:
        try:
            return Source.objects.get(**data)
        except Source.DoesNotExist:
            raise serializers.ValidationError(
                f"Source with name '{data['name']}' does not exist"
                if "name" in data
                else f"Source with id '{data['id']}' does not exist"
            )

    def create(self, validated_data):
        data_sources = validated_data.pop("data_sources", [])

        instance = super().create(validated_data)

        for data_source in data_sources:
            source = self._get_source(data_source)
            instance.data_sources.add(source)

        return instance

    def update(self, instance, validated_data):
        data_sources = validated_data.pop("data_sources", [])

        new_source_ids = []
        existing_source_ids = list(instance.data_sources.values_list("id", flat=True))

        for data_source in data_sources:
            source = self._get_source(data_source)
            instance.data_sources.add(source)
            new_source_ids.append(source.id)

        for source in set(existing_source_ids) - set(new_source_ids):
            instance.data_sources.remove(source)

        return super().update(instance, validated_data)


class NodeSerializer(SourceParentMixin, serializers.ModelSerializer):
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


class SourceDestinationMixin:
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


class EdgeSerializer(SourceParentMixin, SourceDestinationMixin, serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False)
    data_sources = ChildSourceSerializer(many=True, required=False)

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


class SourceChildMixin:
    @cached_property
    def source_model(self) -> Source:
        return Source.objects.get(pk=self.context["view"].kwargs["source_pk"])

    def create(self, validated_data):
        instance = super().create(validated_data)

        self.add_source(instance, self.source_model)

        return instance

    def update(self, instance, validated_data):
        self.add_source(instance, self.source_model)

        return super().update(instance, validated_data)


class SourceMetadataField(JSONField):
    def to_representation(self, value):
        return value.get(self.parent.source_model.name)


class SourceMetadataMixin:
    def create(self, validated_data):
        metadata = validated_data.pop("metadata", {})

        validated_data["metadata"] = {
            "grai": metadata.get("grai", {}),
            self.source_model.name: metadata,
        }

        return super().create(validated_data)

    def update(self, instance, validated_data):
        existing = instance.metadata
        metadata = validated_data.pop("metadata", {})

        grai_metadata = merge(metadata.get("grai", {}), existing.get("grai", {}))
        grai_metadata["tags"] = merge_tags(existing.get("grai", {}).get("tags"), metadata.get("grai", {}).get("tags"))

        instance.metadata = {
            "grai": grai_metadata,
            self.source_model.name: metadata,
        }

        return super().update(instance, validated_data)


class SourceNodeSerializer(SourceMetadataMixin, SourceChildMixin, serializers.ModelSerializer):
    display_name = serializers.CharField(required=False)
    metadata = SourceMetadataField()

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

    def add_source(self, instance: Edge, source: Source):
        source.nodes.add(instance)


class SourceEdgeSerializer(
    SourceMetadataMixin,
    SourceChildMixin,
    SourceDestinationMixin,
    serializers.ModelSerializer,
):
    name = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False)
    metadata = SourceMetadataField()

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

    def add_source(self, instance: Edge, source: Source):
        source.edges.add(instance)
