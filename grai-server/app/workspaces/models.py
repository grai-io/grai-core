import uuid

from django.db import models
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager


class Workspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]


class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        "users.User",
        related_name="memberships",
        on_delete=models.PROTECT,
    )
    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="memberships",
        on_delete=models.PROTECT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "users.User",
        related_name="memberships_created_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "workspace"],
                name="One membership per user per workspace",
            )
        ]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["workspace"]),
        ]


class WorkspaceAPIKeyManager(BaseAPIKeyManager):
    def get_usable_keys(self):
        return super().get_usable_keys()


class WorkspaceAPIKey(AbstractAPIKey):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
    created_by = models.ForeignKey(
        "users.User",
        related_name="workspace_api_keys_created_by",
        on_delete=models.CASCADE,
    )

    objects = WorkspaceAPIKeyManager()

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Workspace API key"
        verbose_name_plural = "Workspace API keys"
