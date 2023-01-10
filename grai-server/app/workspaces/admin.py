from django.contrib import admin

from .models import Membership, Workspace, WorkspaceAPIKey

admin.site.register(Workspace)
admin.site.register(Membership)
admin.site.register(WorkspaceAPIKey)
