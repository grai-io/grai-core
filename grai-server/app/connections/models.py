import uuid

from django.db import models
from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey


class Connector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="Name uniqueness"),
        ]
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["name"]),
        ]


class Connection(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connector = models.ForeignKey(
        "Connector", related_name="connections", on_delete=models.PROTECT
    )
    namespace = models.CharField(max_length=255, default="default")
    name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    secrets = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="connections",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "users.User",
        related_name="connections",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "namespace", "name"],
                name="Node namespaces/name uniqueness - Connection",
            )
        ]
        indexes = [
            models.Index(fields=["workspace", "namespace", "name"]),
        ]


class Run(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connection = TenantForeignKey(
        "Connection", related_name="runs", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="runs",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True,
        null=True,)
    finished_at = models.DateTimeField(blank=True,
        null=True,)
    user = models.ForeignKey(
        "users.User",
        related_name="runs",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
