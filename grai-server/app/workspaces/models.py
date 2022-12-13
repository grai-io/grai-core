import uuid

from django.db import models


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
