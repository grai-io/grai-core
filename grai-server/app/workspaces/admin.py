from django.contrib import admin

from .models import Membership, Organisation, Workspace, WorkspaceAPIKey


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


class WorkspaceAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]


admin.site.register(Organisation)
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Membership)
admin.site.register(WorkspaceAPIKey)
