from django.db.models import fields
from rest_framework import serializers

from .models import Edge, Node


class NodeSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(required=False)

    class Meta:
        model = Node
        fields = (
            "id",
            "namespace",
            "name",
            "display_name",
            "data_source",
            "metadata",
            "is_active",
        )
        read_only_fields = ("created_at", "updated_at")


class EdgeSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(read_only=True)
    # is_active = serializers.BooleanField(read_only=True)
    # metadata = serializers.JSONField(required=False)
    # source = serializers.PrimaryKeyRelatedField(read_only=True, pk_field='id')
    # destination = serializers.PrimaryKeyRelatedField(read_only=True, pk_field='id')

    class Meta:
        model = Edge
        fields = ("id", "data_source", "metadata", "is_active", "source", "destination")
        read_only_fields = ("created_at", "updated_at")
