import json

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from connections.models import Connection


def save(model: Connection):
    cron = model.schedules["cron"]

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=cron["minutes"],  # TODO: Get from schedule
        hour=cron["hours"],
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
        # timezone=zoneinfo.ZoneInfo("Canada/Pacific"),
    )

    if model.task:
        model.task.crontab = schedule
        model.task.kwargs = json.dumps({"connectionId": str(model.id)})
        model.task.enabled = model.is_active
        model.task.save()
    else:
        model.task = PeriodicTask.objects.create(
            crontab=schedule,
            name=f"{model.name}-{str(model.id)}",
            task="connections.tasks.run_connection_schedule",
            kwargs=json.dumps({"connectionId": str(model.id)}),
            enabled=model.is_active,
        )
