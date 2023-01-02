import uuid

from django.db import models
from django.db.models import F, Q
from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey


# Create your models here.
class Node(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    namespace = models.CharField(max_length=255, default="default")
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)

    data_source = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="nodes",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.OneToOneField(
    #     "users.User", related_name="created_by", on_delete=models.PROTECT
    # )

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.name

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.display_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "namespace", "name"],
                name="Node namespaces/name uniqueness",
            )
        ]
        indexes = [
            models.Index(fields=["workspace", "namespace", "name"]),
        ]


class Edge(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    namespace = models.CharField(max_length=255, default="default")
    display_name = models.CharField(max_length=255)

    data_source = models.CharField(max_length=255)
    source = TenantForeignKey(
        "Node", related_name="source_edges", on_delete=models.PROTECT
    )
    destination = TenantForeignKey(
        "Node", related_name="destination_edges", on_delete=models.PROTECT
    )
    metadata = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="edges",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.OneToOneField("users.User", on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = str(self)
        if not self.display_name:
            self.display_name = self.name

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.source} -> {self.destination}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(source=F("destination")),
                name="Edges are not allowed between the same nodes",
            ),
            models.UniqueConstraint(
                fields=["workspace", "namespace", "name"],
                name="Edge namespaces/name uniqueness",
            ),
            models.UniqueConstraint(
                fields=["source", "destination"],
                condition=Q(is_active=True),
                name="one_active_edge_between_nodes",
            ),
        ]
        indexes = [
            models.Index(fields=["workspace", "is_active"]),
            models.Index(fields=["workspace", "namespace", "name"]),
        ]
