from django.db.models import fields
from rest_framework import serializers

from .models import Workspace, Membership


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("created_at", "updated_at")


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            "id",
            "role",
            "is_active",
            "user",
            "workspace",
        )
        read_only_fields = ("created_at", "updated_at", "created_by")
