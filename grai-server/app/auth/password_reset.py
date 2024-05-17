from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import User


class GraiPasswordResetGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp):
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""

        last_reset = user.last_pw_reset()
        if last_reset is None:
            raise Exception("Cannot generate password reset without request attempt")

        reset_timestamp = "" if last_reset is None else last_reset.created_at.replace(microsecond=0, tzinfo=None)

        return f"{user.pk}::{user.password}::{timestamp}::{reset_timestamp}::{email}"


password_reset_generator = GraiPasswordResetGenerator()
