from django.contrib import admin

from .models import Workspace, Membership, WorkspaceAPIKey
from rest_framework_api_key.admin import APIKeyModelAdmin

admin.site.register(Workspace)
admin.site.register(Membership)


@admin.register(WorkspaceAPIKey)
class WorkspaceAPIKeyModelAdmin(APIKeyModelAdmin):
    pass
