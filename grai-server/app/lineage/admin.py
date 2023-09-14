from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import JSONField
from django.urls import reverse
from django.utils.html import format_html

from common.admin.fields.json_widget import PrettyJSONWidget
from connections.models import Connection, Run

from .models import Edge, Event, Filter, Node, Source


@admin.action(description="Force delete selected sources")
def delete_sources(modeladmin, request, queryset):  # pragma: no cover
    sources = queryset

    for source in sources:
        for connection in source.connections.all():
            Run.objects.filter(connection=connection).delete()

            connection.delete()

    queryset.delete()


class EdgeInline(admin.TabularInline):
    model = Edge
    extra = 0

    def has_add_permission(self, request, obj=None):  # pragma: no cover
        return False

    def has_delete_permission(self, request, obj=None):  # pragma: no cover
        return False


class SourceEdgeInline(EdgeInline):
    fk_name = "source"
    verbose_name = "Source Edge"
    verbose_name_plural = "Source Edges"
    fields = [
        "name",
        "namespace",
        "destination",
        "metadata",
        "is_active",
    ]
    readonly_fields = [
        "name",
        "namespace",
        "destination",
        "metadata",
        "is_active",
    ]


class DestinationEdgeInline(EdgeInline):
    fk_name = "destination"
    verbose_name = "Destination Edge"
    verbose_name_plural = "Destination Edges"
    fields = ["name", "namespace", "source", "metadata", "is_active"]
    readonly_fields = [
        "name",
        "namespace",
        "source",
        "metadata",
        "is_active",
    ]


class NodeSourceInline(admin.TabularInline):
    model = Node.data_sources.through
    extra = 0


class EdgeSourceInline(admin.TabularInline):
    model = Edge.data_sources.through
    extra = 0


class NodeAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def final_name(self, obj):
        return obj.display_name if obj.display_name else obj.name

    list_display = (
        "id",
        "namespace",
        "final_name",
        "workspace",
        "is_active",
        "created_at",
    )

    search_fields = ["id", "namespace", "name", "display_name"]

    list_filter = (
        "workspace",
        ("created_at", DateFieldListFilter),
        "namespace",
        "is_active",
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}

    inlines = [
        SourceEdgeInline,
        DestinationEdgeInline,
        NodeSourceInline,
    ]


class EdgeAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def final_name(self, obj):
        return obj.display_name if obj.display_name else obj.name

    list_display = (
        "id",
        "namespace",
        "final_name",
        "workspace",
        "is_active",
        "created_at",
    )

    search_fields = ["id", "namespace", "name", "display_name"]

    list_filter = (
        "workspace",
        ("created_at", DateFieldListFilter),
        "namespace",
        "is_active",
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}

    inlines = [EdgeSourceInline]


class FilterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
    )

    search_fields = ["id", "name"]

    list_filter = (
        "workspace",
        ("created_at", DateFieldListFilter),
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


class ConnectionInline(admin.TabularInline):
    model = Connection
    extra = 0

    fields = [
        "name",
    ]

    def view(self):  # pragma: no cover
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:connections_connection_change", args=(self.id,)),
            self.name,
        )

    fields = ("name", view)
    readonly_fields = [view]


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "workspace",
        "created_at",
    )

    search_fields = ["id", "name"]

    list_filter = (
        "workspace",
        ("created_at", DateFieldListFilter),
    )

    inlines = [
        ConnectionInline,
    ]

    actions = [
        delete_sources,
    ]


admin.site.register(Node, NodeAdmin)
admin.site.register(Edge, EdgeAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Event)
admin.site.register(Source, SourceAdmin)
