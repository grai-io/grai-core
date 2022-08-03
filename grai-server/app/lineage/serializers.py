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
    name = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False)

    class Meta:
        model = Edge
        fields = (
            "id",
            "name",
            "display_name",
            "namespace",
            "data_source",
            "metadata",
            "is_active",
            "source",
            "destination",
        )
        read_only_fields = ("created_at", "updated_at")
