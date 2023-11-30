import uuid

from django.db import models
from django_multitenant.models import TenantModel
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone


class ConnectorSlugs(models.TextChoices):
    POSTGRESQL = "postgres", "Postgres"
    SNOWFLAKE = "snowflake", "Snowflake"
    DBT = "dbt", "dbt"
    DBT_CLOUD = "dbt_cloud", "dbt Cloud"
    YAMLFILE = "yaml_file", "YAML"
    MSSQL = "mssql", "Microsoft SQL Server"
    BIGQUERY = "bigquery", "Google BigQuery"
    FIVETRAN = "fivetran", "Fivetran"
    MYSQL = "mysql", "MySQL"
    REDSHIFT = "redshift", "Amazon Redshift"
    METABASE = "metabase", "Metabase"
    LOOKER = "looker", "Looker"
    OPEN_LINEAGE = "openlineage", "OpenLineage"
    FLAT_FILE = "flatfile", "Flat File"


class ConnectorStatus(models.TextChoices):
    COMING_SOON = "coming_soon", "Coming Soon"
    ALPHA = "alpha", "Alpha"
    BETA = "beta", "beta"
    GENERAL_RELEASE = "general_release", "General Release"


DEFAULT_STATUS_PRIORITY = {
    ConnectorStatus.COMING_SOON: -100,
    ConnectorStatus.ALPHA: 0,
    ConnectorStatus.BETA: 50,
    ConnectorStatus.GENERAL_RELEASE: 100,
}


class ConnectorManager(models.Manager):
    def get_by_natural_key(self, name: str) -> "Connector":
        return self.get(name=name)


class Connector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, choices=ConnectorSlugs.choices, blank=True, null=True)
    metadata = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    events = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=ConnectorStatus.choices, default=ConnectorStatus.GENERAL_RELEASE)
    priority = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ConnectorManager()

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-priority", "name"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="Name uniqueness"),
        ]
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["name"]),
        ]


@receiver(pre_save, sender=Connector)
def update_priority(sender, instance, **kwargs):
    if instance.priority is None:
        instance.priority = DEFAULT_STATUS_PRIORITY.get(instance.status, 100)

    # Handles fixture loading
    if kwargs["raw"]:
        instance.created_at = timezone.now()
        instance.updated_at = instance.created_at


class Connection(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connector = models.ForeignKey("Connector", related_name="connections", on_delete=models.PROTECT)
    namespace = models.CharField(max_length=255, default="default")
    name = models.CharField(max_length=255)
    source = models.ForeignKey(
        "lineage.source",
        related_name="connections",
        on_delete=models.CASCADE,
    )
    metadata = models.JSONField(default=dict)
    secrets = models.JSONField(default=dict, blank=True, null=True)
    schedules = models.JSONField(default=dict, blank=True, null=True)
    task = models.ForeignKey(
        "django_celery_beat.PeriodicTask",
        related_name="connections",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="connections",
        on_delete=models.CASCADE,
    )

    temp = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "users.User",
        related_name="connections",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["workspace", "name"]),
        ]

    def save(self, *args, **kwargs):
        task = None

        if isinstance(self.schedules, dict):
            type = self.schedules.get("type", None)

            if type is None:
                pass

            elif type == "cron":
                from connections.schedules.cron import save

                save(self)

            elif type == "dbt-cloud":
                from connections.schedules.dbt_cloud import save

                save(self)

            else:
                raise Exception("Schedule type not found")

        elif self.task is not None:
            task = self.task
            self.task = None

        super(Connection, self).save(*args, **kwargs)

        if task:
            task.delete()


class Run(TenantModel):
    TESTS = "tests"
    UPDATE = "update"
    VALIDATE = "validate"
    EVENTS = "events"
    EVENTS_ALL = "events_all"

    RUN_ACTIONS = [
        (TESTS, "tests"),
        (UPDATE, "update"),
        (VALIDATE, "validate"),
        (EVENTS, "events"),
        (EVENTS_ALL, "events_all"),
    ]

    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(
        "lineage.Source",
        related_name="runs",
        on_delete=models.CASCADE,
    )
    connection = models.ForeignKey(
        "Connection",
        related_name="runs",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
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
    started_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    finished_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        "users.User",
        related_name="runs",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    trigger = models.JSONField(
        default=dict,
        blank=True,
        null=True,
    )
    input = models.JSONField(
        blank=True,
        null=True,
    )
    commit = models.ForeignKey(
        "installations.Commit",
        related_name="runs",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    action = models.CharField(max_length=255, choices=RUN_ACTIONS, default="update")

    def __str__(self):
        return str(self.id)


def directory_path(instance, filename):
    return "run_{0}/{1}".format(instance.run.id, filename)


class RunFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    run = models.ForeignKey("Run", related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=directory_path, editable=False)
    name = models.CharField(max_length=255, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.file.name

        super(RunFile, self).save(*args, **kwargs)
