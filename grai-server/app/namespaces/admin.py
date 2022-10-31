from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin

from namespaces.models import Namespace, ServiceAPIKey

admin.site.register(Namespace)


@admin.register(ServiceAPIKey)
class NamespaceAPIKeyModelAdmin(APIKeyModelAdmin):
    pass
