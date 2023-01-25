from django.contrib import admin

from .models import Membership, Organisation, Workspace, WorkspaceAPIKey

admin.site.register(Organisation)
admin.site.register(Workspace)
admin.site.register(Membership)
admin.site.register(WorkspaceAPIKey)
