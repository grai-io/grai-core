from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import Count, Q

from lineage.models import Edge, Node

from .models import Membership, Organisation, Workspace, WorkspaceAPIKey


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
    def node_count(self, obj):
        return "{0:,}".format(obj.node_count)

    def connection_count(self, obj):
        return "{0:,}".format(obj.connection_count)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            node_count=Count("nodes", distinct=True),
            connection_count=Count("connections", distinct=True, filter=Q(connections__temp=False)),
        )
        return queryset

    list_display = ("id", "name", "organisation", "node_count", "connection_count", "created_at")

    list_filter = (
        ("created_at", DateFieldListFilter),
        ("organisation", admin.RelatedOnlyFieldListFilter),
        "name",
    )

    search_fields = ["id", "name"]

    inlines = [
        MembershipInline,
    ]

    actions = [empty_workspace]


class OrganisationAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Membership)
admin.site.register(WorkspaceAPIKey)
