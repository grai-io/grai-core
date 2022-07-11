from django.db import models
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager


class NamespaceAPIKeyManager(BaseAPIKeyManager):
    def get_usable_keys(self):
        return super().get_usable_keys().filter(namespace__active=True)


class Namespace(models.Model):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ServiceAPIKey(AbstractAPIKey):
    namespace = models.ForeignKey(
        Namespace,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    objects = NamespaceAPIKeyManager()

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Service API key"
        verbose_name_plural = "Service API keys"
