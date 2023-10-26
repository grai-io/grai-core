import uuid
from enum import Enum

from django.db import models


class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class MessageRoles(ChoicesMixin, Enum):
    USER = "user"
    AGENT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"


class UserChat(models.Model):
    """ """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membership = models.ForeignKey("workspaces.Membership", related_name="membership", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(UserChat, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    visible = models.BooleanField()
    role = models.CharField(max_length=255, choices=MessageRoles.choices(), default=MessageRoles.USER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]
