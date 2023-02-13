from django.db.models import fields

from rest_framework import serializers

from .models import Connection, Connector, Run


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = (
            "id",
            "connector",
            "namespace",
            "name",
            "metadata",
            "is_active",
            "workspace",
        )
        read_only_fields = ("created_at", "updated_at", "created_by")


class ConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connector
        fields = (
            "id",
            "name",
            "metadata",
            "is_active",
        )
        read_only_fields = ("created_at", "updated_at")


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = (
            "id",
            "connection",
            "status",
            "metadata",
            "workspace",
            "user",
        )
        read_only_fields = ("created_at", "updated_at", "started_at", "finished_at")
