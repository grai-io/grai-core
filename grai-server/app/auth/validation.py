from decouple import config
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string

from users.models import User, AuditEvents, Audit
from enum import StrEnum


class CacheKeys(StrEnum):
    PW_RESET = "_cached_last_pw_reset"


def _generate_token(user: User) -> str:
    return verification_generator.make_token(user)


def send_validation_email(user: User):
    reset_event = Audit(user=user, event=AuditEvents.PASSWORD_RESET.name).save()
    setattr(user, CacheKeys.PW_RESET, reset_event)

    token = _generate_token(user)

    c = {
        "base_url": config("FRONTEND_URL", "http://localhost:3000"),
        "token": token,
        "uid": user.pk,
    }
    email_message = render_to_string("auth/email_verification.txt", c)
    html_message = render_to_string("auth/email_verification_template.html", c)

    subject = "Welcome to Grai"

    send_mail(
        subject,
        email_message,
        settings.EMAIL_FROM,
        [user.username],
        fail_silently=False,
        html_message=html_message,
    )


class VerificationGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp):
        """
        Hash the user's primary key, email (if available):

        Running this data through salted_hmac() prevents password cracking
        attempts using the reset token, provided the secret isn't compromised.
        """

        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""

        cached_pw_audit = getattr(user, CacheKeys.PW_RESET, None)

        if cached_pw_audit is None:
            last_reset = cached_pw_audit
        else:
            last_reset = user.last_pw_reset()

        reset_timestamp = "" if last_reset is None else last_reset.created_at.replace(microsecond=0, tzinfo=None)

        return f"{user.pk}{timestamp}{reset_timestamp}{email}"


verification_generator = VerificationGenerator()
