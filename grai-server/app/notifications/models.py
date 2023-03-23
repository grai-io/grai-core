import uuid

from django.db import models
from django_multitenant.models import TenantModel


class Alert(TenantModel):
    SLACK = "slack"
    EMAIL = "email"
    PAGER_DUTY = "pager_duty"

    CHANNELS = [
        (SLACK, "slack"),
        (EMAIL, "email"),
        (PAGER_DUTY, "pager_duty"),
    ]

    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    channel = models.CharField(max_length=255, choices=CHANNELS)
    channel_metadata = models.JSONField(default=dict)
    triggers = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="alerts",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "name"],
                name="Alert unique name per workspace",
            )
        ]
        indexes = [
            models.Index(fields=["workspace"]),
        ]
