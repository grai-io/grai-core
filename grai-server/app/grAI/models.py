from django.db import models
import uuid
from enum import Enum


class UserChat(models.Model):
    """ """

    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    membership = models.ForeignKey("workspaces.Membership", related_name="membership", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["chat_id"]),
        ]


class Message(models.Model):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
    ROLES = [(USER, "user"), (AGENT, "agent"), (SYSTEM, "system")]

    chat = models.ForeignKey(UserChat, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    visible = models.BooleanField()
    role = models.CharField(max_length=255, choices=ROLES, default=USER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]
