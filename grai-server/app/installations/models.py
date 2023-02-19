import uuid

from django.db import models
from django_multitenant.models import TenantModel


class Repository(TenantModel):
    tenant_id = "workspace_id"

    GITHUB = "github"

    REPOSITORY_TYPES = [
        (GITHUB, "github"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField(max_length=255, choices=REPOSITORY_TYPES)
    owner = models.CharField(max_length=255, editable=False)
    repo = models.CharField(max_length=255, editable=False)
    installation_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="repositories",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}/{self.repo}"

    class Meta:
        verbose_name_plural = "repositories"
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "type", "owner", "repo"],
                name="Repository type/owner/repo uniqueness",
            )
        ]
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["type", "owner"]),
            models.Index(fields=["type", "owner", "repo"]),
        ]


class Branch(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="branches",
        on_delete=models.CASCADE,
    )
    repository = models.ForeignKey(
        "installations.Repository",
        related_name="branches",
        on_delete=models.CASCADE,
    )
    reference = models.CharField(max_length=255, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference

    class Meta:
        verbose_name_plural = "branches"
        constraints = [
            models.UniqueConstraint(
                fields=["repository", "reference"],
                name="Branch repository/reference uniqueness",
            )
        ]
        indexes = [
            models.Index(fields=["reference"]),
            models.Index(fields=["repository", "reference"]),
        ]


class PullRequest(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="pull_requests",
        on_delete=models.CASCADE,
    )
    repository = models.ForeignKey(
        "installations.Repository",
        related_name="pull_requests",
        on_delete=models.CASCADE,
    )
    branch = models.ForeignKey(
        "installations.Branch",
        related_name="pull_requests",
        on_delete=models.CASCADE,
    )
    reference = models.CharField(max_length=255, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["repository", "reference"],
                name="Pull Request repository/reference uniqueness",
            )
        ]
        indexes = [
            models.Index(fields=["reference"]),
            models.Index(fields=["repository", "reference"]),
        ]


class Commit(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="commits",
        on_delete=models.CASCADE,
    )
    repository = models.ForeignKey(
        "installations.Repository",
        related_name="commits",
        on_delete=models.CASCADE,
    )
    branch = models.ForeignKey(
        "installations.Branch",
        related_name="commits",
        on_delete=models.CASCADE,
    )
    pull_request = models.ForeignKey(
        "installations.PullRequest",
        related_name="commits",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    reference = models.CharField(max_length=255, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["repository", "reference"],
                name="Commit repository/reference uniqueness",
            )
        ]
        indexes = [
            models.Index(fields=["reference"]),
            models.Index(fields=["repository", "reference"]),
        ]
