from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import JSONField

from common.admin.fields.json_widget import PrettyJSONWidget

from .models import Edge, Event, Filter, Node


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
        "data_source",
        "destination",
        "metadata",
        "is_active",
    ]
    readonly_fields = [
        "name",
        "namespace",
        "data_source",
        "destination",
        "metadata",
        "is_active",
    ]


class DestinationEdgeInline(EdgeInline):
    fk_name = "destination"
    verbose_name = "Destination Edge"
    verbose_name_plural = "Destination Edges"
    fields = ["name", "namespace", "data_source", "source", "metadata", "is_active"]
    readonly_fields = [
        "name",
        "namespace",
        "data_source",
        "source",
        "metadata",
        "is_active",
    ]


class NodeAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def final_name(self, obj):
        return obj.display_name if obj.display_name else obj.name

    list_display = (
        "id",
        "namespace",
        "final_name",
        "data_source",
        "workspace",
        "is_active",
        "created_at",
    )

    search_fields = ["id", "namespace", "name", "display_name", "data_source"]

    list_filter = (
        "workspace",
        ("created_at", DateFieldListFilter),
        "namespace",
        "is_active",
        "data_source",
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}

    inlines = [
        SourceEdgeInline,
        DestinationEdgeInline,
    ]


class EdgeAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def final_name(self, obj):
        return obj.display_name if obj.display_name else obj.name

    list_display = (
        "id",
        "namespace",
        "final_name",
        "data_source",
        "workspace",
        "is_active",
        "created_at",
    )

    search_fields = ["id", "namespace", "name", "display_name", "data_source"]

    list_filter = (
        "workspace",
        ("created_at", DateFieldListFilter),
        "namespace",
        "is_active",
        "data_source",
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


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


admin.site.register(Node, NodeAdmin)
admin.site.register(Edge, EdgeAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Event)
