from django.db import models
import uuid
from enum import Enum


class UserChat(models.Model):
    """ """

    USER = "user"
    AGENT = "agent"

    ROLES = [(USER, "user"), (AGENT, "agent")]

    id = models.AutoField(primary_key=True)
    membership = models.ForeignKey("workspaces.Membership", related_name="membership", on_delete=models.CASCADE)
    chat_id = models.UUIDField(default=uuid.uuid4, editable=False)
    message_number = models.IntegerField(default=0)
    role = models.CharField(max_length=255, choices=ROLES, default=USER)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.chat_id is None:
            self.message_number = None
        elif self.message_number is None:
            max_message_number = UserChat.objects.filter(membership=self.membership, chat_id=self.chat_id).aggregate(
                models.Max("message_number")
            )["message_number__max"]
            self.message_number = max_message_number + 1
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["chat_id", "message_number"],
                name="Message numbers are unique for each chat",
            ),
        ]
        indexes = [
            models.Index(fields=["chat_id"]),
            models.Index(fields=["membership", "created_at"]),
        ]
