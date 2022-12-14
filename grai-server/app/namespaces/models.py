from django.db import models


class Namespace(models.Model):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="namespaces",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
