import uuid

from django.db import models
from django_multitenant.models import TenantModel
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager
from .utils import get_current_user


class Workspace(TenantModel):
    tenant_id = "id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]


class LimitedWorkspaceManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()

        if user:
            return super().get_queryset().filter(memberships__user_id=user.id)

        return super().get_queryset()


class LimitedWorkspace(Workspace):
    class Meta:
        proxy = True


class Membership(TenantModel):
    tenant_id = "workspace_id"

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
