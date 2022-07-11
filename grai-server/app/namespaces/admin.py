from django.contrib import admin
from namespaces.models import Namespace, ServiceAPIKey

from rest_framework_api_key.admin import APIKeyModelAdmin


admin.site.register(Namespace)


@admin.register(ServiceAPIKey)
class NamespaceAPIKeyModelAdmin(APIKeyModelAdmin):
    pass
