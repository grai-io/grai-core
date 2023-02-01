from django.contrib import admin

from .models import Membership, Organisation, Workspace, WorkspaceAPIKey
from lineage.models import Node, Edge


@admin.action(description="Delete nodes and edges")
def empty_workspace(modeladmin, request, queryset):
    workspaces = queryset

    for workspace in workspaces:
        Edge.objects.filter(workspace=workspace).delete()
        Node.objects.filter(workspace=workspace).delete()


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


class WorkspaceAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]

    actions = [empty_workspace]


admin.site.register(Organisation)
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Membership)
admin.site.register(WorkspaceAPIKey)
