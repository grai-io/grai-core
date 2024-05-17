import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from typing import Optional


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Users require a username.")

        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self._create_user(username, password, **extra_fields)

        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class UserAuditMixin:
    def _last_audit_event(self, event: str) -> Optional["Audit"]:
        event_filter = models.Q(user=super().pk, event=event)
        return Audit.objects.filter(event_filter).last()

    def last_pw_reset(self) -> Optional["Audit"]:
        return self._last_audit_event(AuditEvents.PASSWORD_RESET.name)

    def last_logout(self) -> Optional["Audit"]:
        return self._last_audit_event(AuditEvents.LOGOUT.name)


class User(UserAuditMixin, AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    email = None
    first_name = models.CharField(default="", max_length=255)
    last_name = models.CharField(default="", max_length=255)
    phone = PhoneNumberField(null=True, blank=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class AuditEvents(models.TextChoices):
    LOGIN = "login", "login"
    LOGOUT = "logout", "logout"
    PASSWORD_RESET = "password_reset", "Password Reset"


class Audit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        related_name="audits",
        on_delete=models.CASCADE,
    )
    event = models.CharField(max_length=255, choices=AuditEvents.choices)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
