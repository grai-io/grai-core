import uuid

from django.db import models


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


class Connection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connector = models.ForeignKey(
        "Connector", related_name="connections", on_delete=models.PROTECT
    )
    namespace = models.CharField(max_length=255, default="default")
    name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    secrets = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=True)

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
                fields=["namespace", "name"],
                name="Node namespaces/name uniqueness - Connection",
            )
        ]
        indexes = [
            models.Index(fields=["namespace", "name"]),
        ]
