from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.http.request import HttpRequest

from .models import Audit, AuditEvents


def request_to_metadata(request: HttpRequest) -> dict:
    try:
        return dict(request.headers)
    except TypeError:
        return {}


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    Audit.objects.create(
        user=user,
        event=AuditEvents.LOGIN,
        metadata=request_to_metadata(request),
    )


@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    Audit.objects.create(
        user=user,
        event=AuditEvents.LOGOUT,
        metadata=request_to_metadata(request),
    )
