import uuid

from django.db import models
from enum import Enum


class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class MessageRoles(ChoicesMixin, Enum):
    USER = "user"
    AGENT = "assistant"
    SYSTEM = "system"


class MessageActions(ChoicesMixin, Enum):
    SUMMARIZE = "summarize"
    FUNCTION = "function"
    MESSAGE = "message"


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
    action = models.CharField(max_length=255, choices=MessageActions.choices(), default=MessageActions.MESSAGE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]
