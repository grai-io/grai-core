from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.html import format_html

from lineage.extended_graph_cache import ExtendedGraphCache
from lineage.models import Edge, Node

from .models import Membership, Organisation, Workspace, WorkspaceAPIKey


@admin.action(description="Delete nodes and edges")
def empty_workspace(modeladmin, request, queryset):  # pragma: no cover
    workspaces = queryset

    for workspace in workspaces:
        edges = Edge.objects.filter(workspace=workspace)

        if edges.exists():
            edges._raw_delete(edges.db)

        nodes = Node.objects.filter(workspace=workspace)

        if nodes.exists():
            nodes._raw_delete(nodes.db)

        cache = ExtendedGraphCache(workspace)
        cache.clear_cache()


@admin.action(description="Enable search")
def enable_search(modeladmin, request, queryset):  # pragma: no cover
    queryset.update(search_enabled=True)


@admin.action(description="Disable search")
def disable_search(modeladmin, request, queryset):  # pragma: no cover
    queryset.update(search_enabled=False)


@admin.action(description="Build workspace cache")
def build_workspace_cache(modeladmin, request, queryset):  # pragma: no cover
    workspaces = queryset

    for workspace in workspaces:
        cache = ExtendedGraphCache(workspace)
        cache.build_cache()


@admin.action(description="Clear workspace cache")
def clear_workspace_cache(modeladmin, request, queryset):  # pragma: no cover
    workspaces = queryset

    for workspace in workspaces:
        cache = ExtendedGraphCache(workspace)
        cache.clear_cache()


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


class WorkspaceAdmin(admin.ModelAdmin):
    def node_count(self, obj):  # pragma: no cover
        return "{0:,}".format(obj.node_count)

    def connection_count(self, obj):  # pragma: no cover
        return "{0:,}".format(obj.connection_count)

    def get_queryset(self, request):  # pragma: no cover
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            node_count=Count("nodes", distinct=True),
            connection_count=Count("connections", distinct=True, filter=Q(connections__temp=False)),
        )
        return queryset.all()

    list_display = (
        "id",
        "name",
        "organisation",
        "node_count",
        "connection_count",
        "search_enabled",
        "created_at",
    )

    list_filter = (
        ("created_at", DateFieldListFilter),
        ("organisation", admin.RelatedOnlyFieldListFilter),
        "search_enabled",
        "name",
    )

    search_fields = ["id", "name", "organisation__name"]

    inlines = [
        MembershipInline,
    ]

    actions = [
        empty_workspace,
        enable_search,
        disable_search,
        build_workspace_cache,
        clear_workspace_cache,
    ]


class WorkspaceInline(admin.TabularInline):
    model = Workspace
    extra = 0

    def view(self):  # pragma: no cover
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:workspaces_workspace_change", args=(self.id,)),
            self.name,
        )

    fields = ("name", view)
    readonly_fields = (view,)


class OrganisationAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]

    inlines = [
        WorkspaceInline,
    ]


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Membership)
admin.site.register(WorkspaceAPIKey)
