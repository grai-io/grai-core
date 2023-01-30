import json
import uuid

from django.db import models
from django_multitenant.fields import TenantForeignKey
from django_multitenant.models import TenantModel


class Connector(models.Model):
    POSTGRESQL = "PostgreSQL"
    SNOWFLAKE = "Snowflake"
    DBT = "dbt"
    YAMLFILE = "YAML File"

    CONNECTOR_CHOICES = [
        (POSTGRESQL, "PostgreSQL"),
        (SNOWFLAKE, "Snowflake"),
        (DBT, "dbt"),
        (YAMLFILE, "YAML File"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, choices=CONNECTOR_CHOICES)
    metadata = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    coming_soon = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
    connector = models.ForeignKey("Connector", related_name="connections", on_delete=models.PROTECT)
    namespace = models.CharField(max_length=255, default="default")
    name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    secrets = models.JSONField(default=dict, blank=True, null=True)
    schedules = models.JSONField(default=dict, blank=True, null=True)
    task = models.ForeignKey(
        "django_celery_beat.PeriodicTask",
        related_name="connections",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
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
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

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

    def save(self, *args, **kwargs):
        if isinstance(self.schedules, dict):

            type = self.schedules.get("type", None)

            if type is None:
                pass

            elif type == "cron":
                from django_celery_beat.models import CrontabSchedule, PeriodicTask

                cron = self.schedules["cron"]

                schedule, _ = CrontabSchedule.objects.get_or_create(
                    minute=cron["minutes"],  # TODO: Get from schedule
                    hour=cron["hours"],
                    day_of_week="*",
                    day_of_month="*",
                    month_of_year="*",
                    # timezone=zoneinfo.ZoneInfo("Canada/Pacific"),
                )

                if self.task:
                    self.task.crontab = schedule
                    self.task.kwargs = json.dumps({"connectionId": str(self.id)})
                    self.task.enabled = self.is_active
                    self.task.save()
                else:
                    self.task = PeriodicTask.objects.create(
                        crontab=schedule,
                        name=f"{self.name}-{str(self.id)}",
                        task="connections.tasks.run_connection_schedule",
                        kwargs={"connectionId": str(self.id)},
                        enabled=self.is_active,
                    )
            else:
                raise Exception("Schedule type not found")

        # elif self.task:
        #     self.task.delete()

        super(Connection, self).save(*args, **kwargs)


class Run(TenantModel):
    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connector = models.ForeignKey("Connector", related_name="runs", on_delete=models.PROTECT)
    connection = TenantForeignKey(
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

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.connector_id is None and self.connection_id is not None:
            self.connector = self.connection.connector

        super(Run, self).save(*args, **kwargs)


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
