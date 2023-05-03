import json
import uuid

from django.db import models
from django_multitenant.fields import TenantForeignKey
from django_multitenant.models import TenantModel


class Connector(models.Model):
    POSTGRESQL = "postgres"
    SNOWFLAKE = "snowflake"
    DBT = "dbt"
    DBT_CLOUD = "dbt_cloud"
    YAMLFILE = "yaml_file"
    MSSQL = "mssql"
    BIGQUERY = "bigquery"
    FIVETRAN = "fivetran"
    MYSQL = "mysql"
    REDSHIFT = "redshift"

    CONNECTOR_SLUGS = [
        (POSTGRESQL, "postgres"),
        (SNOWFLAKE, "snowflake"),
        (DBT, "dbt"),
        (DBT_CLOUD, "dbt_cloud"),
        (YAMLFILE, "yaml_file"),
        (MSSQL, "mssql"),
        (BIGQUERY, "bigquery"),
        (FIVETRAN, "fivetran"),
        (MYSQL, "mysql"),
        (REDSHIFT, "redshift"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, choices=CONNECTOR_SLUGS, blank=True, null=True)
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
                        kwargs=json.dumps({"connectionId": str(self.id)}),
                        enabled=self.is_active,
                    )

            elif type == "dbt-cloud":
                import requests

                schedule = self.schedules.get("dbt_cloud")

                assert schedule is not None

                base_url = "https://cloud.getdbt.com/api"

                headers = {
                    "Authorization": f"Token {self.secrets.get('api_key')}",
                }

                data = {
                    "event_types": ["job.run.completed"],
                    "name": "Grai Webhook",
                    "client_url": "https://7bfa-82-4-89-233.ngrok-free.app/api/v1/dbt-cloud/",
                    "active": True,
                    "description": "A webhook for when jobs are completed",
                    "job_ids": [int(schedule.get("job_id"))],
                }

                print(schedule)

                webhook_id = schedule.get("webhook_id")

                if webhook_id:
                    account_id = schedule.get("account_id")
                    assert account_id is not None

                    url = f"{base_url}/v3/accounts/{account_id}/webhooks/subscription/{webhook_id}"
                    response = requests.put(url, json=data, headers=headers)

                    if response.status_code != 200:
                        message = f"Error: {response.status_code}. {response.content.decode()}"
                        raise Exception(message)

                else:
                    response = requests.get(f"{base_url}/v2/accounts", headers=headers)
                    account_id = response.json().get("data")[0].get("id")

                    url = f"{base_url}/v3/accounts/{account_id}/webhooks/subscriptions"

                    response = requests.post(url, json=data, headers=headers)

                    if response.status_code != 201:
                        message = f"Error: {response.status_code}. {response.content.decode()}"
                        raise Exception(message)

                    response_data = response.json().get("data")
                    assert response_data is not None

                    schedule.update(
                        {
                            "webhook_id": response_data.get("id"),
                            "hmac_secret": response_data.get("hmac_secret"),
                            "account_id": account_id,
                        }
                    )
                    self.schedules.update({"dbt_cloud": schedule})
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

    RUN_ACTIONS = [
        (TESTS, "tests"),
        (UPDATE, "update"),
        (VALIDATE, "validate"),
    ]

    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connection = TenantForeignKey(
        "Connection",
        related_name="runs",
        on_delete=models.CASCADE,
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
