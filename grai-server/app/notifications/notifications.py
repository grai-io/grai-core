from celery import shared_task

from .channels.email_channel import EmailChannel
from .models import Alert


def get_alerts(trigger: str):
    filter_name = f"triggers__{trigger}"
    return Alert.objects.filter(**{filter_name: True})


def get_channel(channel: str):
    if channel == "email":
        return EmailChannel()

    else:
        raise Exception(f"Notification channel {channel} not supported")


@shared_task
def send_notification(trigger: str, message: str):
    alerts = get_alerts(trigger)

    for alert in alerts:
        channel = get_channel(alert.channel)
        channel.send(message, alert)
