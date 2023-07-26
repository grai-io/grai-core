from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from notifications.models import Alert

from .base_channel import BaseChannel


class EmailChannel(BaseChannel):
    def send(self, message: str, alert: Alert):
        emails = alert.channel_metadata.get("emails", [])

        c = {
            "message": message,
        }
        email_message = render_to_string("notifications/notification_template.txt", c)

        subject = "Grai Notification"

        send_mail(
            subject,
            email_message,
            settings.EMAIL_FROM,
            emails,
            fail_silently=False,
        )
