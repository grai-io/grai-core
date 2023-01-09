from django.contrib import admin

from .models import Workspace, Membership, WorkspaceAPIKey

admin.site.register(Workspace)
admin.site.register(Membership)
admin.site.register(WorkspaceAPIKey)
